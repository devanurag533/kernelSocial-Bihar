import streamlit as st
from PIL import Image
import datetime
from supabase import create_client, Client

# --- SUPABASE CONNECTION SETUP ---
# Ye wahi details hain jo humne setup ki thi
URL = "https://shqcptzsxfvfoinjchwv.supabase.co"
KEY = "sb_publishable_aJJXzqC-ucvDDBZygeDddw_hAsGWN_K"
supabase: Client = create_client(URL, KEY)

# Page Configuration
st.set_page_config(page_title="KernelSocial Bihar", page_icon="🌾", layout="centered")

# Custom CSS for Instagram-like feel
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008080; color: white; }
    .main { background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# Session States to track login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- DATABASE FUNCTIONS ---
def login_user(username, password):
    try:
        res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        return len(res.data) > 0
    except Exception as e:
        st.error(f"Login Error: {e}")
        return False

def signup_user(username, password):
    try:
        # Check if user already exists
        check = supabase.table("users").select("*").eq("username", username).execute()
        if len(check.data) > 0:
            return "exists"
        
        # Insert new user
        supabase.table("users").insert({"username": username, "password": password}).execute()
        return "success"
    except Exception as e:
        return str(e)

# --- USER INTERFACE (UI) ---

if not st.session_state.logged_in:
    # --- LOGIN / SIGNUP SCREEN ---
    st.title("🌾 KernelSocial Bihar")
    st.subheader("Bihar ka apna safe social platform")
    
    choice = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)

    if choice == "Login":
        u_name = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Log In"):
            if login_user(u_name, u_pass):
                st.session_state.logged_in = True
                st.session_state.current_user = u_name
                st.success(f"Welcome back, {u_name}!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    else:
        new_u = st.text_input("Choose a Username")
        new_p = st.text_input("Choose a Password", type="password")
        if st.button("Create My Account"):
            if new_u and new_p:
                status = signup_user(new_u, new_p)
                if status == "success":
                    st.success("Account ban gaya! Ab aap Login kar sakte hain.")
                elif status == "exists":
                    st.warning("Ye username pehle se kisi ne le liya hai.")
                else:
                    st.error(f"Error: {status}")
            else:
                st.warning("Please fill all fields")

else:
    # --- MAIN APP (AFTER LOGIN) ---
    st.sidebar.title(f"👤 {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # Post Upload Section
    st.sidebar.divider()
    st.sidebar.header("📤 Naya Post Dalein")
    uploaded_file = st.sidebar.file_uploader("Select Photo", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.sidebar.image(img, caption="Preview", use_container_width=True)
        cap = st.sidebar.text_area("Caption likhein (Strictly No Vulgarity)")
        
        if st.sidebar.button("Post to Feed"):
            # Yahan hum temporary post dikhayenge (Permanent ke liye Supabase Storage chahiye hoga)
            if 'temp_posts' not in st.session_state:
                st.session_state.temp_posts = []
            
            post_data = {
                "user": st.session_state.current_user,
                "image": img,
                "caption": cap,
                "time": datetime.datetime.now().strftime("%d %b, %H:%M")
            }
            st.session_state.temp_posts.insert(0, post_data)
            st.sidebar.success("Aapka post live hai!")

    # --- MAIN FEED ---
    st.title("📸 Social Feed")
    st.write(f"Namaste **{st.session_state.current_user}**! Dekhiye Bihar mein kya naya hai.")
    st.divider()

    if 'temp_posts' not in st.session_state or not st.session_state.temp_posts:
        st.info("Abhi feed khali hai. Kuch accha post karke shuruat karein!")
    else:
        for post in st.session_state.temp_posts:
            with st.container():
                st.markdown(f"### 👤 {post['user']}")
                st.image(post['image'], use_container_width=True)
                st.write(f"**{post['user']}**: {post['caption']}")
                st.caption(f"📅 {post['time']}")
                st.divider()
