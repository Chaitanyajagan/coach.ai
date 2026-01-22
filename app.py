import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

import database as db
from langchain_utils import InterviewCoach
from styles import get_global_styles
from views.auth import page_login_signup
from views.setup import render_home_view
from views.interview import render_interview_view
from views.result import render_result_view

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pro Interview Coach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL STYLES ---
st.markdown(get_global_styles(), unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_data' not in st.session_state:
    st.session_state.interview_data = {}
if 'coach' not in st.session_state:
    st.session_state.coach = InterviewCoach()
if "camera_on" not in st.session_state:
    st.session_state.camera_on = True

# --- DB INIT ---
db.init_db()

# --- ENTRY POINT ---
if not st.session_state.auth_status:
    # PAGE 1: LOGIN/SIGNUP
    page_login_signup()
else:
    # Initialize View State if missing
    if 'dash_view' not in st.session_state:
        st.session_state.dash_view = 'setup'

    # --- SIDEBAR (Status Only) ---
    with st.sidebar:
        st.markdown("### ⚡ Coach.AI")
        st.caption(f"Logged in as {st.session_state.current_user}")
        
        # API Key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.text_input("Gemini API Key", type="password")
        if api_key:
            st.session_state.coach.configure(api_key)
            
        st.divider()
        st.markdown("**Current Step:**")
        if st.session_state.dash_view == 'setup':
            st.info("2. Job Setup")
        elif st.session_state.dash_view == 'interview':
            st.warning("3. Interview")
        elif st.session_state.dash_view == 'result':
            st.success("4. Results")
            
        st.divider()
        if st.button("Log Out"):
            st.session_state.auth_status = False
            st.session_state.dash_view = 'setup'
            st.rerun()

    # --- MAIN ROUTER (Strict Flow) ---
    if st.session_state.dash_view == 'setup' or st.session_state.dash_view == 'home':
         # PAGE 2: SETUP
         render_home_view()
         
    elif st.session_state.dash_view == 'interview':
         # PAGE 3: INTERVIEW
         render_interview_view()
         
    elif st.session_state.dash_view == 'result':
         # PAGE 4: RESULT
         render_result_view()
    else:
         # Fallback
         st.session_state.dash_view = 'setup'
         st.rerun()
