import streamlit as st
from PIL import Image
import datetime
from supabase import create_client, Client

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="KernelSocial Bihar", 
    page_icon="📸", 
    layout="centered"
)

# --- 2. ATTRACTIVE CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #008080; font-weight: bold; text-align: center; }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        height: 3em; 
        background-color: #008080; 
        color: white; 
        font-weight: bold; 
        border: none;
    }
    .post-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SUPABASE CONNECTION (ERROR FREE) ---
# Secrets check karne ka robust tarika
if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    try:
        supabase: Client = create_client(URL, KEY)
    except Exception as e:
        st.error(f"Connection failed: {e}")
        st.stop()
else:
    st.error("⚠️ Secrets not found! Go to Streamlit Cloud Settings > Secrets and add SUPABASE_URL and SUPABASE_KEY.")
    st.stop()

# --- 4. SESSION STATES ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- 5. DATABASE FUNCTIONS ---
def login_user(username, password):
    try:
        res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        return len(res.data) > 0
    except:
        return False

def signup_user(username, password):
    try:
        check = supabase.table("users").select("*").eq("username", username).execute()
        if len(check.data) > 0: return False
        supabase.table("users").insert({"username": username, "password": password}).execute()
        return True
    except:
        return False

# --- 6. USER INTERFACE ---

if not st.session_state.logged_in:
    # --- LOGIN / SIGNUP SCREEN ---
    st.markdown("<h1 class='main-title'>📸 KernelSocial Bihar</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Clean Content. Safe Community.</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])
    
    with tab1:
        u_name = st.text_input("Username", key="l_user")
        u_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Log In"):
            if login_user(u_name, u_pass):
                st.session_state.logged_in = True
                st.session_state.current_user = u_name
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        n_user = st.text_input("Choose Username", key="s_user")
        n_pass = st.text_input("Choose Password", type="password", key="s_pass")
        if st.button("Create Account"):
            if n_user and n_pass:
                if signup_user(n_user, n_pass):
                    st.success("Account created! Now go to Login tab.")
                else:
                    st.warning("Username already exists.")
            else:
                st.error("Please fill all fields.")

else:
    # --- LOGGED IN: FEED & UPLOAD ---
    st.sidebar.title(f"👋 Namaste, {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()
    st.sidebar.header("📤 Naya Post")
    up_file = st.sidebar.file_uploader("Select Photo", type=['jpg','png','jpeg'])
    
    if up_file:
        img = Image.open(up_file)
        st.sidebar.image(img, use_container_width=True)
        cap = st.sidebar.text_area("Caption...")
        if st.sidebar.button("Post Karein"):
            if 'feed' not in st.session_state: st.session_state.feed = []
            st.session_state.feed.insert(0, {
                "user": st.session_state.current_user,
                "img": img,
                "cap": cap,
                "time": datetime.datetime.now().strftime("%I:%M %p")
            })
            st.success("Post live ho gaya!")

    # --- MAIN FEED ---
    st.title("📸 Social Feed")
    if 'feed' not in st.session_state or not st.session_state.feed:
        st.info("Abhi feed khali hai. Pehla post aap karein!")
    else:
        for post in st.session_state.feed:
            with st.container():
                st.markdown(f"**👤 {post['user']}**")
                st.image(post['img'], use_container_width=True)
                st.write(post['cap'])
                st.caption(f"🕒 {post['time']}")
                st.divider()
