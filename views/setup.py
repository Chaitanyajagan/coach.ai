import streamlit as st
import streamlit as st

def render_home_view():
    st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Configure your interview session</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Simple Centered Layout
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        # 1. Job Description Presets
        JD_PRESETS = {
            "Software Developer": """
            Role: Software Developer
            Key Skills: Python, JavaScript, React, REST APIs, SQL, Git.
            Responsibilities:
            - Design and build scalable web applications.
            - Write clean, maintainable code.
            - Collaborate with cross-functional teams.
            - Experience with cloud platforms (AWS/GCP) is a plus.
            """,
            "Data Scientist": """
            Role: Data Scientist
            Key Skills: Python, Pandas, Scikit-learn, TensorFlow/PyTorch, SQL, Data Visualization.
            Responsibilities:
            - Analyze large datasets to extract actionable insights.
            - Build predictive models and machine learning algorithms.
            - Communicate findings to stakeholders.
            """,
            "Product Manager": """
            Role: Product Manager
            Key Skills: Agile/Scrum, User Story Mapping, Roadmap Planning, Stakeholder Management.
            Responsibilities:
            - Define product vision and strategy.
            - Prioritize features based on user needs and business goals.
            - Work closely with engineering and design teams.
            """,
            "General / Document Based": """
            Role: Subject Matter Expert / General Interview
            Key Skills: Understanding of the provided document context.
            Responsibilities:
            - Discuss the content of the uploaded document.
            - Answer questions related to the document's topic.
            - Demonstrate comprehension of the material.
            """
        }
        
        selected_role = st.selectbox("🎯 Select Target Role", list(JD_PRESETS.keys()), index=None, placeholder="Choose a position...")
        
        if selected_role:
            job_desc = JD_PRESETS[selected_role]
            st.success(f"**Selected:** {selected_role}")
        else:
            job_desc = None
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Resume Upload
        resume_file = st.file_uploader("📂 Upload Resume (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
        if resume_file:
            st.info("Resume Attached")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        start_btn = st.button("🚀 Start Interview", type="primary", use_container_width=True)

        if start_btn:
            if not job_desc:
                st.error("Please select a Job Role.")
            elif not resume_file:
                st.error("Please upload your Resume.")
            else:
                try:
                    # Process Resume using OCR Utils
                    from ocr_utils import process_resume_upload
                    resume_text = process_resume_upload(resume_file)
                    
                    # Process 2: Chunking (as requested)
                    from chunking_utils import chunk_text
                    # "Store under a temporary library" -> Session State
                    st.session_state['resume_chunks'] = chunk_text(resume_text)
                    st.toast(f"Resume processed into {len(st.session_state['resume_chunks'])} chunks.")
                    
                    # Store in session
                    st.session_state.interview_data['role'] = selected_role
                    st.session_state.interview_data['job_desc'] = job_desc
                    st.session_state.interview_data['resume_text'] = resume_text
                    st.session_state.messages = []
                    
                    # Reset Flags
                    st.session_state['shutup'] = False
                    st.session_state.camera_on = True # Reset camera too
                    
                    # Generate First Question
                    with st.spinner("Analyzing Resume & JD..."):
                        initial = st.session_state.coach.get_response(
                            role=selected_role,
                            resume_text=resume_text,
                            job_desc=job_desc
                        )
                        st.session_state.messages.append({"role": "assistant", "content": initial['message']})
                        
                        # Generate Audio for Interview View
                        from utils import text_to_speech_file
                        audio_bytes = text_to_speech_file(initial['message'])
                        if audio_bytes:
                            st.session_state['latest_audio'] = audio_bytes
                        
                        # Navigate using dash_view
                        st.session_state.dash_view = 'interview'
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error reading resume: {e}")
