import streamlit as st
from PIL import Image

from ai_copy import generate_copy
from comparison_engine import PriceEntry, compare_prices, parse_csv_text
from comparison_poster import image_to_png_bytes as comparison_png_bytes, render_comparison_poster
from formats import FORMATS, render_social
from poster_engine import calculate_discount, image_to_png_bytes, render_poster

st.set_page_config(page_title="AI Price Poster Maker", page_icon="🛍️", layout="wide")

st.title("🛍️ AI Price Poster Maker")
st.caption("Create sale creatives and compare prices from one simple app.")

mode = st.sidebar.radio("Mode", ["Sale Poster", "Price Comparison"])

if mode == "Sale Poster":
    with st.sidebar:
        st.header("Product details")
        product_name = st.text_input("Product name", "Premium Product")
        mrp = st.number_input("MRP (₹)", min_value=1.0, value=999.0, step=10.0)
        sale_price = st.number_input("Sale price (₹)", min_value=0.0, value=799.0, step=10.0)
        template = st.selectbox("Base template", ["Bold Sale", "Minimal", "Shop Offer"])
        social_format = st.selectbox("Export format", list(FORMATS))
        use_ollama = st.checkbox("Use local Ollama for AI copy", value=True, help="Falls back automatically if Ollama is not running.")
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
        social_poster = render_social(
            base_poster,
            copy["headline"],
            copy["subheadline"],
            copy["cta"],
            sale_price,
            mrp,
            discount,
            FORMATS[social_format],
        )

    left, right = st.columns([1, 1])
    with left:
        st.subheader("AI marketing copy")
        st.write(f"**{copy['headline']}**")
        st.write(copy["subheadline"])
        st.code(copy["cta"], language=None)
        st.metric("Discount", f"{discount}% OFF")
        st.caption("V2 includes local AI copy and lightweight smart background cleanup for plain-background product shots.")

    with right:
        st.subheader("Final poster")
        st.image(social_poster, use_container_width=True)
        st.download_button(
            "⬇️ Download PNG",
            data=image_to_png_bytes(social_poster),
            file_name="sale-poster.png",
            mime="image/png",
            use_container_width=True,
        )

    with st.expander("Original product photo"):
        st.image(product_image, use_container_width=True)

else:
    st.header("V3 — Price Comparison")
    st.write("Enter prices from different stores, or import a CSV, and generate a comparison poster.")

    product_name = st.text_input("Product name", "Product")
    uploaded = st.file_uploader("Optional product photo", type=["png", "jpg", "jpeg", "webp"], key="comparison_image")

    st.subheader("Store prices")
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
            csv_entries = parse_csv_text(csv_file.getvalue().decode("utf-8-sig"))
            entries = csv_entries
            st.success(f"Loaded {len(entries)} valid price rows from CSV.")
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

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Price ranking")
        for index, entry in enumerate(result["entries"], start=1):
            marker = " 🏆 BEST DEAL" if entry == result["cheapest"] else ""
            st.write(f"**{index}. {entry.store}** — ₹{entry.price:,.2f}{marker}")

        st.download_button(
            "⬇️ Download comparison PNG",
            data=comparison_png_bytes(poster),
            file_name="price-comparison.png",
            mime="image/png",
            use_container_width=True,
        )

    with right:
        st.subheader("Comparison poster")
        st.image(poster, use_container_width=True)
