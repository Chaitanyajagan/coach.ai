import streamlit as st

from textwrap import dedent

def render_result_view():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>Interview Analysis Request</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
    
    # Center the result card
    c_main = st.container()
    
    with c_main:
        # Display Final Verdict from AI if available, else Mock
        verdict = st.session_state.interview_data.get('verdict', 'Pending Analysis')
        score = st.session_state.interview_data.get('final_score', 0)
        
        # Native Streamlit Components (Foolproof)
        st.markdown("### 🏁 Interview Completed")
        st.caption("Great job completing the session. Here is your summary.")
        st.divider()
        
        col_score, col_verdict = st.columns(2)
        with col_score:
            st.metric(label="Final Score", value=f"{score}/10")
        with col_verdict:
            st.info(f"**Verdict:** {verdict}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered Return Button
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Return to Dashboard", type="primary", use_container_width=True):
            st.session_state.dash_view = 'home'
            st.rerun()
