import streamlit as st
import requests

URL = "https://fakestoreapi.com/products"


try:
    response = requests.get(URL)
    response.raise_for_status()
    products = response.json()

except requests.RequestException:
    st.error("Failed to load products")
    st.stop()

st.title("Fake store products")

st.sidebar.header("filters")

categories = ["All"]

for product in products:
    if product["category"] not in categories:
        categories.append(product["category"])

category = st.sidebar.selectbox("Category", categories)

maximum = max(product["price"] for product in products)

maximum_price = st.sidebar.slider("Maximum Price", 0.0, float(maximum), float(maximum))

search = st.sidebar.text_input("Search")

filtered_products = []

for product in products:

    if category != "All" and product["category"] != category:
        continue

    if product["price"] > maximum_price:
        continue

    if search.lower() not in product["title"].lower():
        continue

    filtered_products.append(product)


for product in filtered_products:

    st.header(product["title"])

    st.write("ID:", product["id"])
    st.write("Price:", "$" + str(product["price"]))
    st.write("Category:", product["category"])
    st.write("Rating:", product["rating"]["rate"])
    st.write("Rating count:", product["rating"]["count"])
    st.write("Image:", product["image"])

    with st.expander("View details"):
        st.write(product["description"])