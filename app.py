import streamlit as st
from PIL import Image

from poster_engine import calculate_discount, image_to_png_bytes, render_poster

st.set_page_config(page_title="AI Price Poster Maker", page_icon="🛍️", layout="wide")

st.title("🛍️ AI Price Poster Maker")
st.caption("Create a ready-to-post sale poster from one product photo and a few details.")

with st.sidebar:
    st.header("Poster details")
    product_name = st.text_input("Product name", "Premium Product")
    mrp = st.number_input("MRP (₹)", min_value=1.0, value=999.0, step=10.0)
    sale_price = st.number_input("Sale price (₹)", min_value=0.0, value=799.0, step=10.0)
    template = st.selectbox("Template", ["Bold Sale", "Minimal", "Shop Offer"])
    uploaded = st.file_uploader("Product photo", type=["png", "jpg", "jpeg", "webp"])

if sale_price > mrp:
    st.error("Sale price cannot be greater than MRP.")
    st.stop()

if not uploaded:
    st.info("Upload a product photo in the sidebar to generate your first poster.")
    st.stop()

product_image = Image.open(uploaded)
discount = calculate_discount(mrp, sale_price)

poster = render_poster(product_image, product_name.strip() or "Product", mrp, sale_price, template)

left, right = st.columns([1, 1])
with left:
    st.subheader("Product")
    st.image(product_image, use_container_width=True)
with right:
    st.subheader("Poster preview")
    st.image(poster, use_container_width=True)
    st.metric("Discount", f"{discount}% OFF")
    st.download_button(
        "⬇️ Download PNG",
        data=image_to_png_bytes(poster),
        file_name="sale-poster.png",
        mime="image/png",
        use_container_width=True,
    )
