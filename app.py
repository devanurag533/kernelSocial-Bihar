import streamlit as st
from PIL import Image
import datetime
from supabase import create_client, Client

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="KernelSocial Bihar", 
    page_icon="📸", 
    layout="centered"
)

# --- CUSTOM CSS FOR ATTRACTIVE UI ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Post card style */
    .post-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border: 1px solid #eee;
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background-color: #008080;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #006666;
        border: none;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }
    h1, h2, h3 {
        color: #1a1a1a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SUPABASE CONNECTION ---
# Streamlit Secrets se data uthayega
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error("Secrets not configured correctly in Streamlit Cloud!")

# --- SESSION STATES ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- APP LOGIC ---
def login_user(username, password):
    res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    return len(res.data) > 0

def signup_user(username, password):
    check = supabase.table("users").select("*").eq("username", username).execute()
    if len(check.data) > 0: return False
    supabase.table("users").insert({"username": username, "password": password}).execute()
    return True

# --- UI RENDERING ---

if not st.session_state.logged_in:
    # --- LOGIN / SIGNUP PAGE ---
    st.image("https://img.icons8.com/clouds/200/000000/instagram-new.png", width=100)
    st.title("KernelSocial Bihar")
    st.markdown("##### Clean Content. Safe Community.")
    
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])
    
    with tab1:
        u_name = st.text_input("Username", placeholder="Enter your username")
        u_pass = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Login"):
            if login_user(u_name, u_pass):
                st.session_state.logged_in = True
                st.session_state.current_user = u_name
                st.rerun()
            else:
                st.error("Oops! Galat details hain.")

    with tab2:
        n_user = st.text_input("Choose Username", placeholder="Unique name rakhein")
        n_pass = st.text_input("Choose Password", type="password", placeholder="Strong password rakhein")
        if st.button("Create Account"):
            if n_user and n_pass:
                if signup_user(n_user, n_pass):
                    st.success("Account ban gaya! Ab Login tab par jayein.")
                else:
                    st.warning("Ye naam pehle se hai.")
            else:
                st.error("Sabhi fields bharein.")

else:
    # --- LOGGED IN: FEED & UPLOAD ---
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Namaste, {st.session_state.current_user}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.header("📸 New Post")
        up_file = st.file_uploader("Choose a photo", type=['jpg','png','jpeg'])
        if up_file:
            img = Image.open(up_file)
            st.image(img, caption="Preview", use_container_width=True)
            cap = st.text_area("Write caption...")
            if st.button("Publish Now"):
                # Temporary feed update
                if 'feed' not in st.session_state: st.session_state.feed = []
                st.session_state.feed.insert(0, {
                    "user": st.session_state.current_user,
                    "img": img,
                    "cap": cap,
                    "time": datetime.datetime.now().strftime("%I:%M %p")
                })
                st.success("Post Live ho gaya!")

    # Main Feed UI
    st.title("📸 Feed")
    
    if 'feed' not in st.session_state or not st.session_state.feed:
        st.info("Abhi tak yahan kuch nahi hai. Pehle insaan baniye jo post karein!")
    else:
        for post in st.session_state.feed:
            # HTML for nice Card Look
            st.markdown(f"""
                <div class="post-card">
                    <p style='font-weight: bold; font-size: 1.1em;'>👤 {post['user']}</p>
                </div>
            """, unsafe_allow_html=True)
            st.image(post['img'], use_container_width=True)
            st.markdown(f"**{post['user']}**: {post['cap']}")
            st.caption(f"🕒 Posted at {post['time']}")
            st.markdown("<br>", unsafe_allow_html=True)
