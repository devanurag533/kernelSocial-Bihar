import streamlit as st
from PIL import Image
import datetime

# Page Settings
st.set_page_config(page_title="EcoSocial Bihar", page_icon="🌾")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008080; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 EcoSocial Bihar")
st.subheader("Bihar ka apna safe social platform")

# --- SIDEBAR: Post Creation ---
st.sidebar.header("Naya Post Banayein")
uploaded_file = st.sidebar.file_uploader("Photo select karein", type=['jpg', 'png', 'jpeg'])

# Vulgarity Check Placeholder
def check_safety(img):
    # Abhi ke liye ye sab allow kar raha hai, 
    # baad mein hum isme AI Model add karenge.
    return True

if uploaded_file:
    img = Image.open(uploaded_file)
    if check_safety(img):
        st.sidebar.image(img, caption="Preview", use_container_width=True)
        cap = st.sidebar.text_area("Caption likhein...")
        if st.sidebar.button("Post Karein"):
            if 'posts' not in st.session_state:
                st.session_state.posts = []
            
            data = {"img": img, "cap": cap, "date": datetime.datetime.now().strftime("%d %b, %H:%M")}
            st.session_state.posts.insert(0, data)
            st.sidebar.success("Post live ho gaya!")
    else:
        st.sidebar.error("Warning: Vulgar content allow nahi hai!")

# --- MAIN FEED ---
st.write("---")
if 'posts' not in st.session_state or not st.session_state.posts:
    st.info("Abhi tak koi post nahi hai. Pehla post aap karein!")
else:
    for p in st.session_state.posts:
        with st.container():
            st.image(p['img'], use_container_width=True)
            st.write(f"**Caption:** {p['cap']}")
            st.caption(f"📅 {p['date']}")
            st.write("---")
