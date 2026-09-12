import streamlit as st
from PIL import Image

from ai_copy import generate_copy
from batch_engine import build_batch_posters, parse_product_csv, posters_to_zip
from comparison_engine import PriceEntry, compare_prices, parse_csv_text
from comparison_poster import image_to_png_bytes as comparison_png_bytes, render_comparison_poster
from creative_engine import generate_variations
from formats import FORMATS, render_social
from poster_engine import calculate_discount, image_to_png_bytes, render_poster

st.set_page_config(page_title="AI Price Poster Maker", page_icon="🛍️", layout="wide")
st.title("🛍️ AI Price Poster Maker")
st.caption("Create sale creatives, compare prices, generate branded batches, and make AI creative variations.")
mode = st.sidebar.radio("Mode", ["Sale Poster", "Price Comparison", "Batch Business", "AI Creative Lab"])

if mode == "Sale Poster":
    with st.sidebar:
        st.header("Product details")
        product_name = st.text_input("Product name", "Premium Product")
        mrp = st.number_input("MRP (₹)", min_value=1.0, value=999.0, step=10.0)
        sale_price = st.number_input("Sale price (₹)", min_value=0.0, value=799.0, step=10.0)
        template = st.selectbox("Base template", ["Bold Sale", "Minimal", "Shop Offer"])
        social_format = st.selectbox("Export format", list(FORMATS))
        use_ollama = st.checkbox("Use local Ollama for AI copy", value=True)
        uploaded = st.file_uploader("Product photo", type=["png", "jpg", "jpeg", "webp"])
    if sale_price > mrp:
        st.error("Sale price cannot be greater than MRP.")
        st.stop()
    if not uploaded:
        st.info("Upload a product photo in the sidebar to generate a poster.")
        st.stop()
    product_image = Image.open(uploaded).convert("RGB")
    discount = calculate_discount(mrp, sale_price)
    name = product_name.strip() or "Product"
    with st.spinner("Generating your creative..."):
        copy = generate_copy(name, discount, use_ollama=use_ollama)
        base_poster = render_poster(product_image, name, mrp, sale_price, template)
        social_poster = render_social(base_poster, copy["headline"], copy["subheadline"], copy["cta"], sale_price, mrp, discount, FORMATS[social_format])
    left, right = st.columns(2)
    with left:
        st.subheader("AI marketing copy")
        st.write(f"**{copy['headline']}**")
        st.write(copy["subheadline"])
        st.code(copy["cta"], language=None)
        st.metric("Discount", f"{discount}% OFF")
    with right:
        st.subheader("Final poster")
        st.image(social_poster, use_container_width=True)
        st.download_button("⬇️ Download PNG", data=image_to_png_bytes(social_poster), file_name="sale-poster.png", mime="image/png", use_container_width=True)

elif mode == "Price Comparison":
    st.header("V3 — Price Comparison")
    product_name = st.text_input("Product name", "Product")
    uploaded = st.file_uploader("Optional product photo", type=["png", "jpg", "jpeg", "webp"], key="comparison_image")
    entries: list[PriceEntry] = []
    for i in range(5):
        c1, c2 = st.columns([2, 1])
        store = c1.text_input(f"Store {i + 1}", "" if i else "Store A", key=f"store_{i}")
        price = c2.number_input(f"Price {i + 1} (₹)", min_value=0.0, value=0.0, step=10.0, key=f"price_{i}")
        if store.strip() and price > 0:
            entries.append(PriceEntry(store, price))
    csv_file = st.file_uploader("Or import CSV (store,price)", type=["csv"], key="comparison_csv")
    if csv_file is not None:
        try:
            entries = parse_csv_text(csv_file.getvalue().decode("utf-8-sig"))
        except (UnicodeDecodeError, ValueError) as exc:
            st.error(str(exc))
    if not entries:
        st.info("Add at least one store and a price to generate a comparison.")
        st.stop()
    try:
        result = compare_prices(entries)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    a, b, c = st.columns(3)
    a.metric("Best price", f"₹{result['cheapest'].price:,.0f}", result["cheapest"].store)
    b.metric("Highest price", f"₹{result['highest'].price:,.0f}", result["highest"].store)
    c.metric("Maximum saving", f"₹{result['savings']:,.0f}", f"{result['savings_percent']:.2f}%")
    product_image = Image.open(uploaded).convert("RGB") if uploaded else None
    poster = render_comparison_poster(product_name, entries, product_image)
    left, right = st.columns(2)
    with left:
        st.subheader("Price ranking")
        for index, entry in enumerate(result["entries"], 1):
            marker = " 🏆 BEST DEAL" if entry == result["cheapest"] else ""
            st.write(f"**{index}. {entry.store}** — ₹{entry.price:,.2f}{marker}")
        st.download_button("⬇️ Download comparison PNG", data=comparison_png_bytes(poster), file_name="price-comparison.png", mime="image/png", use_container_width=True)
    with right:
        st.subheader("Comparison poster")
        st.image(poster, use_container_width=True)

elif mode == "Batch Business":
    st.header("V4 — Batch Business Mode")
    st.write("Create consistent branded sale posters for a product catalog and download them as one ZIP.")
    with st.sidebar:
        brand_name = st.text_input("Business / brand name", "Your Store")
        brand_color = st.color_picker("Brand color", "#111111")
        template = st.selectbox("Poster template", ["Bold Sale", "Minimal", "Shop Offer"], key="batch_template")
        logo_file = st.file_uploader("Optional logo", type=["png", "jpg", "jpeg", "webp"], key="batch_logo")
    catalog_file = st.file_uploader("Product catalog CSV", type=["csv"], key="batch_catalog")
    image_files = st.file_uploader("Product images (filenames must match image_name)", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="batch_images")
    if catalog_file is None:
        st.info("Upload a catalog CSV to start the batch generator.")
        st.stop()
    try:
        products = parse_product_csv(catalog_file.getvalue().decode("utf-8-sig"))
    except (UnicodeDecodeError, ValueError) as exc:
        st.error(str(exc))
        st.stop()
    image_map = {file.name: Image.open(file).convert("RGB") for file in image_files}
    missing = [p.image_name for p in products if p.image_name not in image_map]
    if missing:
        st.warning(f"Missing {len(missing)} image(s): {', '.join(missing[:8])}")
        st.stop()
    logo = Image.open(logo_file).convert("RGBA") if logo_file else None
    product_pairs = [(p, image_map[p.image_name]) for p in products]
    with st.spinner(f"Generating {len(product_pairs)} branded posters..."):
        posters = build_batch_posters(product_pairs, template, brand_name, brand_color, logo)
        zip_data = posters_to_zip(posters)
    st.success(f"Generated {len(posters)} posters successfully.")
    st.download_button("⬇️ Download all posters (ZIP)", data=zip_data, file_name="branded-posters.zip", mime="application/zip", use_container_width=True)
    st.subheader("Preview")
    preview_columns = st.columns(min(3, len(posters)))
    for column, (filename, poster) in zip(preview_columns, posters[:3]):
        with column:
            st.image(poster, caption=filename, use_container_width=True)

else:
    st.header("V5 — AI Creative Lab")
    st.write("Generate three distinct promotional poster variations from one product photo and AI marketing copy.")
    with st.sidebar:
        product_name = st.text_input("Product name", "Premium Product", key="creative_name")
        mrp = st.number_input("MRP (₹)", min_value=1.0, value=999.0, step=10.0, key="creative_mrp")
        sale_price = st.number_input("Sale price (₹)", min_value=0.0, value=799.0, step=10.0, key="creative_sale")
        use_ollama = st.checkbox("Use local Ollama for copy", value=True, key="creative_ollama")
        uploaded = st.file_uploader("Product photo", type=["png", "jpg", "jpeg", "webp"], key="creative_image")
    if sale_price > mrp:
        st.error("Sale price cannot be greater than MRP.")
        st.stop()
    if not uploaded:
        st.info("Upload a product photo to generate variations.")
        st.stop()
    product_image = Image.open(uploaded).convert("RGB")
    discount = calculate_discount(mrp, sale_price)
    name = product_name.strip() or "Product"
    with st.spinner("Creating AI variations..."):
        copy = generate_copy(name, discount, use_ollama=use_ollama)
        variations = generate_variations(product_image, name, mrp, sale_price, discount, copy["headline"], copy["cta"])
    st.success("3 creative variations generated.")
    cols = st.columns(3)
    for col, (variation_name, poster) in zip(cols, variations.items()):
        with col:
            st.subheader(variation_name)
            st.image(poster, use_container_width=True)
            st.download_button("⬇️ Download", data=image_to_png_bytes(poster), file_name=f"{variation_name.lower().replace(' ', '-')}.png", mime="image/png", use_container_width=True)
    st.caption(f"AI headline: {copy['headline']} · CTA: {copy['cta']}")
