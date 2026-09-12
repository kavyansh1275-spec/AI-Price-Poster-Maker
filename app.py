import streamlit as st
from PIL import Image

from ai_copy import generate_copy
from formats import FORMATS, render_social
from poster_engine import calculate_discount, image_to_png_bytes, render_poster

st.set_page_config(page_title="AI Price Poster Maker", page_icon="🛍️", layout="wide")

st.title("🛍️ AI Price Poster Maker")
st.caption("Turn a product photo + price into ready-to-post sale creatives.")

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
    st.caption("V2 also includes lightweight smart background cleanup in the image engine for plain-background product shots.")

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
