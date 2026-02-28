import streamlit as st
import database as db

def page_login_signup():
    # Helper to keep login/signup simple in this unified view
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown(f"""
        <div class="glass-card animate-fade-in" style="text-align: center;">
            <h1 style="color: var(--heading-color); margin-bottom: 10px;">Coach.AI</h1>
            <p style="margin-bottom: 20px; color: var(--text-secondary);">AI-Powered Technical Interview Simulator</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    uid = db.verify_user(u, p)
                    if uid:
                        st.session_state.auth_status = True
                        st.session_state.current_user = u
                        st.session_state.current_user_id = uid
                        st.session_state.dash_view = 'setup'
                        st.rerun()
                    else:
                        st.error("Invalid credentials")


