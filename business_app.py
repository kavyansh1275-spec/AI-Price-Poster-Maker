import streamlit as st

from business_workflow import PACKAGES, delivery_checklist, package_quote, quote_text, sales_message

st.set_page_config(page_title="Poster Maker — Business Toolkit", page_icon="💼", layout="wide")
st.title("💼 Business Toolkit")
st.caption("Turn poster generation into a simple local-business offer, quote, and sales workflow.")

with st.sidebar:
    st.header("Client")
    client = st.text_input("Client name", "Rahul")
    business = st.text_input("Business name", "ABC Store")
    package = st.selectbox("Package", list(PACKAGES))
    discount = st.slider("Negotiation discount (%)", 0, 30, 0)
    turnaround = st.selectbox("Turnaround", ["24 hours", "48 hours", "3 days", "5 days"])

quote = package_quote(package, client, business, discount, turnaround)
spec = PACKAGES[package]

c1, c2, c3 = st.columns(3)
c1.metric("Package price", f"₹{spec['price']:,}")
c2.metric("Posters", spec["posters"])
c3.metric("Client total", f"₹{quote.total:,.0f}")

left, right = st.columns(2)
with left:
    st.subheader("Client quote")
    st.code(quote_text(quote), language=None)
    st.download_button("⬇️ Download quote", quote_text(quote), file_name="client-quote.txt", mime="text/plain", use_container_width=True)

with right:
    st.subheader("Ready-to-send sales message")
    st.code(sales_message(quote), language=None)
    st.download_button("⬇️ Download message", sales_message(quote), file_name="sales-message.txt", mime="text/plain", use_container_width=True)

st.divider()
st.subheader("Delivery checklist")
for item in delivery_checklist():
    st.checkbox(item, key=f"check_{item}")

st.info("Workflow: find a local shop → show one sample poster → offer a package → collect product assets → generate → deliver → ask for a testimonial/referral.")
