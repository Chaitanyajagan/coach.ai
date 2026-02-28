import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

import database as db
from langchain_utils import InterviewCoach
from styles import get_global_styles, inject_theme_toggle
from views.auth import page_login_signup
from views.setup import render_home_view
from views.ats_score import render_ats_score_view
from views.interview import render_interview_view
from views.result import render_result_view
from views.history import render_history_view

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pro Interview Coach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL STYLES ---
st.markdown(get_global_styles(), unsafe_allow_html=True)
inject_theme_toggle()

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
if "current_score" not in st.session_state:
    st.session_state.current_score = 0.0

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
            st.session_state.coach.configure(api_key.strip())
            
        st.divider()
        st.markdown("<div class='animate-fade-in delay-2'>", unsafe_allow_html=True)
        st.markdown("**Current Step:**")
        if st.session_state.dash_view == 'setup':
            st.info("2. Job Setup")
        elif st.session_state.dash_view == 'ats_score':
            st.info("3. ATS Resume Eval")
        elif st.session_state.dash_view == 'interview':
            st.warning("4. Interview")
        elif st.session_state.dash_view == 'result':
            st.success("5. Results")
        elif st.session_state.dash_view == 'history':
            st.info("📚 History")
        st.markdown("</div>", unsafe_allow_html=True)
            
        st.divider()
        if st.button("📚 History View", use_container_width=True):
            st.session_state.dash_view = 'history'
            st.rerun()
            
        st.divider()
        if st.button("Log Out", use_container_width=True):
            st.session_state.auth_status = False
            st.session_state.dash_view = 'setup'
            st.rerun()

    # --- MAIN ROUTER (Strict Flow) ---
    if st.session_state.dash_view == 'setup' or st.session_state.dash_view == 'home':
         # PAGE 2: SETUP
         render_home_view()
         
    elif st.session_state.dash_view == 'ats_score':
         # PAGE 3: ATS Score
         render_ats_score_view()
         
    elif st.session_state.dash_view == 'interview':
         # PAGE 4: INTERVIEW
         render_interview_view()
         
    elif st.session_state.dash_view == 'result':
         # PAGE 5: RESULT
         render_result_view()
         
    elif st.session_state.dash_view == 'history':
         # PAGE 6: HISTORY
         render_history_view()
    else:
         # Fallback
         st.session_state.dash_view = 'setup'
         st.rerun()
