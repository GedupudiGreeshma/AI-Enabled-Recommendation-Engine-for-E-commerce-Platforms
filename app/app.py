import streamlit as st
import pickle
import pandas as pd
import os
import random

st.set_page_config(page_title="AI Store", layout="wide")

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.product-card {
    background-color: #111827;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    transition: transform 0.3s ease;
}
.product-card:hover {
    transform: scale(1.05);
}
.price {
    font-size: 18px;
    font-weight: bold;
    color: #22c55e;
}
.rating {
    color: gold;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_data
def load_model():
    base_dir = os.path.dirname(__file__)   # app/ directory
    model_path = os.path.join(base_dir, "recommender_model.pkl")

    with open(model_path, "rb") as f:
        return pickle.load(f)

model_data = load_model()
train_matrix = model_data["train_matrix"]
train_matrix.columns = train_matrix.columns.str.strip()

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 Login to AI Store")

    username = st.text_input("Enter User ID")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):

        if username in train_matrix.index and password == "1234":
            st.session_state.logged_in = True
            st.session_state.user_id = username
            st.rerun()

        elif username not in train_matrix.index:
            st.error("User not found in dataset")

        else:
            st.error("Incorrect password")

# -----------------------------
# MAIN APP
# -----------------------------
else:

    user_id = st.session_state.user_id

    # Helpers
    def normalize(text):
        return text.lower().replace(" ", "").replace("-", "")

    def get_image_path(product):
        base_dir = os.path.dirname(__file__)
        filename = normalize(product) + ".png"
        path = os.path.join(base_dir, "images", filename)
        return path if os.path.exists(path) else None

    def get_price(product):
        random.seed(product)
        return random.randint(20, 500)

    def get_rating(product):
        random.seed(product)
        return round(random.uniform(3.5, 5.0), 1)

    # Category Map
    category_map = {
        "lipstick": "💄 Makeup",
        "foundation": "💄 Makeup",
        "moisturizer": "💄 Makeup",
        "perfume": "💄 Makeup",
        "laptop": "💻 Electronics",
        "smartphone": "💻 Electronics",
        "smartwatch": "💻 Electronics",
        "headphones": "💻 Electronics",
        "curtains": "🏠 Home Decor",
        "lamp": "🏠 Home Decor",
        "cushions": "🏠 Home Decor",
        "wallart": "🏠 Home Decor",
        "jeans": "👕 Clothing",
        "jacket": "👕 Clothing",
        "shoes": "👕 Clothing",
        "tshirt": "👕 Clothing",
        "biography": "📚 Books",
        "comics": "📚 Books",
        "fiction": "📚 Books",
        "nonfiction": "📚 Books",
        "dumbbells": "🏋️ Fitness",
        "resistancebands": "🏋️ Fitness",
        "yogamat": "🏋️ Fitness",
        "treadmill": "🏋️ Fitness"
    }

    # -----------------------------
    # RECOMMENDATION FUNCTIONS
    # -----------------------------
    def recommend_for_user(user_id, top_k=4):
        user_vector = train_matrix.loc[user_id]
        bought = user_vector[user_vector > 0].index.tolist()
        similarity = train_matrix.dot(user_vector).sort_values(ascending=False)

        recommendations = []
        for other_user in similarity.index[1:]:
            other_products = train_matrix.loc[other_user]
            for product in other_products[other_products > 0].index:
                if product not in bought and product not in recommendations:
                    recommendations.append(product)
            if len(recommendations) >= top_k:
                break

        return recommendations[:top_k]

    def similar_products(product, top_k=4):
        norm = normalize(product)
        if norm not in category_map:
            return []
        category = category_map[norm]

        return [
            p for p in train_matrix.columns
            if p != product
            and normalize(p) in category_map
            and category_map[normalize(p)] == category
        ][:top_k]

    def also_bought(product, top_k=4):
        users = train_matrix[train_matrix[product] > 0].index
        if len(users) == 0:
            return []
        co = train_matrix.loc[users].sum().drop(product)
        return co.sort_values(ascending=False).head(top_k).index.tolist()

    # -----------------------------
    # SIDEBAR CART
    # -----------------------------
    st.sidebar.write(f"👤 Logged in as: {user_id}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.selected_product = None
        st.session_state.cart = []
        st.rerun()

    st.sidebar.title("🛒 Cart")

    if st.session_state.cart:
        total = 0
        for item in st.session_state.cart:
            price = get_price(item)
            total += price
            st.sidebar.write(f"{item} - ${price}")
        st.sidebar.write("---")
        st.sidebar.write(f"### Total: ${total}")
    else:
        st.sidebar.write("Cart is empty")

    # -----------------------------
    # HOME PAGE = ONLY CATALOG
    # -----------------------------
    if st.session_state.selected_product is None:

        st.title("🛍️ Product Catalog")

        products = train_matrix.columns.tolist()
        grouped = {}

        for product in products:
            norm = normalize(product)
            category = category_map.get(norm, "Others")
            grouped.setdefault(category, []).append(product)

        for category, items in grouped.items():
            st.markdown(f"## {category}")
            cols = st.columns(4)

            for i, product in enumerate(items):
                with cols[i % 4]:
                    image_path = get_image_path(product)
                    if image_path:
                        st.image(image_path, use_container_width=True)
                    if st.button(product, key=f"catalog_{product}"):
                        st.session_state.selected_product = product
                        st.rerun()

            st.markdown("---")

    # -----------------------------
    # PRODUCT DETAIL PAGE
    # -----------------------------
    else:

        product = st.session_state.selected_product

        if st.button("⬅ Back to Catalog"):
            st.session_state.selected_product = None
            st.rerun()

        st.header(product)

        image_path = get_image_path(product)
        if image_path:
            st.image(image_path, width=350)

        st.write(f"### 💲 Price: ${get_price(product)}")
        st.write(f"### ⭐ Rating: {get_rating(product)}")

        if st.button("Add to Cart"):
            if product not in st.session_state.cart:
                st.session_state.cart.append(product)
                train_matrix.loc[user_id, product] = 1
                st.success("Added to cart!")

        st.markdown("---")

        # Similar
        st.subheader("🔎 Similar Products")
        sim = similar_products(product)
        if sim:
            cols = st.columns(len(sim))
            for i, item in enumerate(sim):
                with cols[i]:
                    img = get_image_path(item)
                    if img:
                        st.image(img, use_container_width=True)
                    if st.button(item, key=f"sim_{item}"):
                        st.session_state.selected_product = item
                        st.rerun()

        st.markdown("---")

        # Also Bought
        st.subheader("🛒 Users Who Bought This Also Bought")
        also = also_bought(product)
        if also:
            cols = st.columns(len(also))
            for i, item in enumerate(also):
                with cols[i]:
                    img = get_image_path(item)
                    if img:
                        st.image(img, use_container_width=True)
                    if st.button(item, key=f"also_{item}"):
                        st.session_state.selected_product = item
                        st.rerun()

        st.markdown("---")

        # Recommended For User (ONLY HERE)
        st.subheader("⭐ Recommended For You")
        personal = recommend_for_user(user_id)
        if personal:
            cols = st.columns(len(personal))
            for i, item in enumerate(personal):
                with cols[i]:
                    img = get_image_path(item)
                    if img:
                        st.image(img, use_container_width=True)
                    if st.button(item, key=f"personal_{item}"):
                        st.session_state.selected_product = item
                        st.rerun()