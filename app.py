import streamlit as st
from PIL import Image
import datetime

# Page Settings
st.set_page_config(page_title="KernelSocial Bihar", page_icon="🌾")

# --- DATABASE SIMULATION (Abhi ke liye temporary) ---
if 'user_db' not in st.session_state:
    st.session_state.user_db = {} # Format: {username: password}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- LOGIN / SIGNUP LOGIC ---
def login_page():
    st.title("🔐 Welcome to KernelSocial")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u_name = st.text_input("Username", key="login_user")
        u_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if u_name in st.session_state.user_db and st.session_state.user_db[u_name] == u_pass:
                st.session_state.logged_in = True
                st.session_state.current_user = u_name
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with tab2:
        new_u_name = st.text_input("Choose Username", key="reg_user")
        new_u_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        if st.button("Create Account"):
            if new_u_name in st.session_state.user_db:
                st.warning("User already exists!")
            elif new_u_name == "" or new_u_pass == "":
                st.error("Fields cannot be empty")
            else:
                st.session_state.user_db[new_u_name] = new_u_pass
                st.success("Account created! Please Login.")

# --- MAIN APP ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar with Logout
    st.sidebar.title(f"👋 Hello, {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- UPLOAD SECTION ---
    st.sidebar.header("📤 Naya Post")
    uploaded_file = st.sidebar.file_uploader("Photo select karein", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.sidebar.image(img, caption="Preview", use_container_width=True)
        cap = st.sidebar.text_area("Caption likhein...")
        if st.sidebar.button("Post Karein"):
            if 'posts' not in st.session_state:
                st.session_state.posts = []
            
            data = {
                "user": st.session_state.current_user,
                "img": img, 
                "cap": cap, 
                "date": datetime.datetime.now().strftime("%d %b, %H:%M")
            }
            st.session_state.posts.insert(0, data)
            st.success("Post live ho gaya!")

    # --- FEED ---
    st.title("🌾 KernelSocial Bihar")
    st.write("---")
    if 'posts' not in st.session_state or not st.session_state.posts:
        st.info("Feed khali hai. Kuch post karein!")
    else:
        for p in st.session_state.posts:
            with st.container():
                st.write(f"👤 **{p['user']}**")
                st.image(p['img'], use_container_width=True)
                st.write(f"{p['cap']}")
                st.caption(f"📅 {p['date']}")
                st.write("---")
