import streamlit as st
import time
import base64

def render_ats_score_view():
    # Inject Custom CSS for the UI
    st.markdown("""
        <style>
        .ats-header-card {
            background-color: var(--ats-card-bg);
            border-right: 1px solid var(--ats-border);
            padding: 15px;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-radius: 4px;
        }
        .ats-header-val {
            font-size: 24px;
            font-weight: bold;
            color: var(--ats-text-primary);
        }
        .ats-header-sub {
            font-size: 11px;
            font-weight: bold;
            padding-top: 5px;
            text-transform: uppercase;
        }
        .ats-sub-red { color: #f44336; }
        .ats-sub-orange { color: #ff9800; }
        .ats-sub-green { color: #4caf50; }
        .overall-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 4px solid #ff9800;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: bold;
            margin: 0 auto;
            color: var(--ats-text-primary);
            background: var(--ats-circle-bg);
        }
        .ats-progress-bar {
            width: 100%;
            height: 15px;
            background: linear-gradient(to right, #f44336, #ff9800, #4caf50);
            border-radius: 10px;
            margin-top: 20px;
            position: relative;
        }
        .ats-marker {
            position: absolute;
            top: -10px;
            width: 0; 
            height: 0; 
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-top: 15px solid var(--ats-text-primary);
            transform: translateX(-50%);
        }
        .ats-resume-container {
            background: var(--ats-resume-bg);
            padding: 30px;
            border-radius: 0 0 5px 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
            color: var(--ats-resume-text);
            height: 80vh;
            overflow-y: auto;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        .ats-resume-container p { margin-bottom: 5px; }
        .highlight-green { background-color: var(--ats-highlight-green); color: var(--ats-highlight-text); padding: 0 2px; }
        .highlight-orange { background-color: var(--ats-highlight-orange); color: var(--ats-highlight-text); padding: 0 2px; }
        .highlight-red { background-color: var(--ats-highlight-red); color: var(--ats-highlight-text); padding: 0 2px; }
        </style>
    """, unsafe_allow_html=True)

    # Check if we have the data
    if 'interview_data' not in st.session_state or 'resume_text' not in st.session_state.interview_data:
        st.warning("No resume data found. Please go back to Job Setup to upload your resume.")
        if st.button("Go to Setup", use_container_width=True):
            st.session_state.dash_view = 'setup'
            st.rerun()
        return

    # Calculate ATS score if not already done
    if 'ats_result' not in st.session_state:
        with st.spinner("Analyzing Resume against Job Description locally..."):
            from utils import calculate_ats_score_local
            ats_result = calculate_ats_score_local(
                resume_text=st.session_state.interview_data['resume_text'],
                job_desc=st.session_state.interview_data['job_desc']
            )
            st.session_state.ats_result = ats_result
    
    ats_result = st.session_state.ats_result
    score = ats_result.get("score", 0)
    
    # Mocking category scores for UI fidelity
    impact_score = max(0, score - 12)
    brevity_score = min(100, score + 15)
    style_score = max(0, score - 16)
    skills_score = min(100, score + 35)

    def get_color_class(s):
        if s >= 80: return "ats-sub-green", "EXCELLENT", "#4caf50"
        if s >= 50: return "ats-sub-orange", "GOOD START", "#ff9800"
        return "ats-sub-red", "NEEDS WORK", "#f44336"

    o_c, o_t, o_hex = get_color_class(score)
    i_c, i_t, i_hex = get_color_class(impact_score)
    b_c, b_t, b_hex = get_color_class(brevity_score)
    s_c, s_t, s_hex = get_color_class(style_score)
    sk_c, sk_t, sk_hex = get_color_class(skills_score)

    user_name = "Candidate" # In a real app, this would be extraced from resume

    # Main Split View
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        # Top Stats Row
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""
                <div class="ats-header-card animate-fade-in delay-1">
                    <div class="overall-circle floating-element" style="border-color: {o_hex}">{score}</div>
                    <div style="font-size: 10px; font-weight: bold; margin-top: 5px; color: var(--ats-text-secondary);">OVERALL</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="ats-header-card animate-fade-in delay-2"><div style="font-size: 12px; font-weight: bold; color: var(--ats-text-secondary); margin-bottom: 10px;">IMPACT</div><div class="ats-header-val">{impact_score}<span style="font-size:14px; color:var(--ats-text-secondary);">/100</span></div><div class="ats-header-sub {i_c}">{i_t}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="ats-header-card animate-fade-in delay-3"><div style="font-size: 12px; font-weight: bold; color: var(--ats-text-secondary); margin-bottom: 10px;">BREVITY</div><div class="ats-header-val">{brevity_score}<span style="font-size:14px; color:var(--ats-text-secondary);">/100</span></div><div class="ats-header-sub {b_c}">{b_t}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="ats-header-card animate-fade-in delay-4"><div style="font-size: 12px; font-weight: bold; color: var(--ats-text-secondary); margin-bottom: 10px;">STYLE</div><div class="ats-header-val">{style_score}<span style="font-size:14px; color:var(--ats-text-secondary);">/100</span></div><div class="ats-header-sub {s_c}">{s_t}</div></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="ats-header-card animate-fade-in delay-5" style="border-right: none;"><div style="font-size: 12px; font-weight: bold; color: var(--ats-text-secondary); margin-bottom: 10px;">SKILLS</div><div class="ats-header-val">{skills_score}<span style="font-size:14px; color:var(--ats-text-secondary);">/100</span></div><div class="ats-header-sub {sk_c}">{sk_t}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Welcome Section
        st.markdown(f"<h2>Good evening, {user_name}.</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--ats-text-secondary); font-size: 16px;'>Welcome to your resume review.</p>", unsafe_allow_html=True)
        
        # Score Bar Section
        st.markdown(f"""
            <div style="background: var(--ats-card-bg); padding: 25px; border-radius: 8px; border: 1px solid var(--ats-border); margin-top: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: var(--ats-text-primary);">Your resume scored {score} out of 100.</h3>
                    <button style="background: var(--msg-bg); color: var(--accent); border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 12px;">💡 EXPLAIN MY SCORE</button>
                </div>
                <!-- Progress bar track -->
                <div class="ats-progress-bar">
                    <div class="ats-marker" style="left: {score}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px; font-weight: bold; color: var(--ats-text-secondary); position: relative;">
                    <span>0</span>
                    <span style="position: absolute; left: {score}%; transform: translateX(-50%); top: -20px; font-size: 11px; color:var(--ats-text-primary);">YOUR RESUME</span>
                    <span>100</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations Section
        st.markdown("""
            <div style="background: var(--ats-card-bg); padding: 25px; border-radius: 8px; border: 1px solid var(--ats-border);">
                <h4 style="color: var(--ats-text-secondary); letter-spacing: 1px; margin-top: 0;">RECOMMENDATIONS</h4>
                <p style="color: var(--ats-text-secondary);">There's room for improvement on your resume. Here are the top fixes you should make to improve its score and success rate.</p>
        """, unsafe_allow_html=True)
        
        missing_kw = ats_result.get("missing_keywords", [])
        if missing_kw:
            st.markdown(f"""
                <div style="border: 1px solid var(--ats-border); border-left: 4px solid #ff9800; padding: 15px; border-radius: 4px; display: flex; align-items: center; margin-bottom: 10px; background: var(--ats-circle-bg);">
                    <div style="background: var(--ats-recommendation-number); width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold; color: var(--ats-recommendation-number-text);">1</div>
                    <div style="flex-grow: 1; font-weight: bold; color:var(--ats-text-primary);">Missing Key Skills</div>
                    <div style="background: rgba(100,221,23,0.1); color: #64dd17; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">SKILLS</div>
                </div>
                <p style="font-size: 12px; color: var(--ats-text-secondary); margin-left: 45px;">Add these keywords: {', '.join(missing_kw[:5])}</p>
            """, unsafe_allow_html=True)
            
        st.markdown("""
                <div style="border: 1px solid var(--ats-border); border-left: 4px solid #f44336; padding: 15px; border-radius: 4px; display: flex; align-items: center; margin-bottom: 10px; background: var(--ats-circle-bg);">
                    <div style="background: var(--ats-recommendation-number); width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold; color: var(--ats-recommendation-number-text);">2</div>
                    <div style="flex-grow: 1; font-weight: bold; color:var(--ats-text-primary);">Impact descriptions could be stronger</div>
                    <div style="background: rgba(255,82,82,0.1); color: #ff5252; padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold;">IMPACT</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.warning("⚠️ **Caution:** The interview consists of 5 questions. You must complete the entire interview for your results and score to be saved. Quitting in the middle will result in lost progress.")
        
        # Flow Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔙 Back to Setup", use_container_width=True):
                if 'ats_result' in st.session_state: del st.session_state['ats_result']
                st.session_state.dash_view = 'setup'
                st.rerun()
        with col2:
            if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
                if st.button("🚀 Proceed to Interview", type="primary", use_container_width=True):
                    with st.spinner("Preparing the first interview question..."):
                        initial = st.session_state.coach.get_response(
                            role=st.session_state.interview_data['role'],
                            resume_text=st.session_state.interview_data['resume_text'],
                            job_desc=st.session_state.interview_data['job_desc']
                        )
                        if 'messages' not in st.session_state:
                            st.session_state.messages = []
                        st.session_state.messages.append({"role": "assistant", "content": initial['message']})
                        
                        from utils import text_to_speech_file
                        audio_bytes = text_to_speech_file(initial['message'])
                        if audio_bytes: st.session_state['latest_audio'] = audio_bytes
                        
                        st.session_state.dash_view = 'interview'
                        st.rerun()
            else:
                if st.button("▶️ Resume Interview", type="primary", use_container_width=True):
                    st.session_state.dash_view = 'interview'
                    st.rerun()

    # Document Viewer Container
    with right_col:
        st.markdown("""
            <div style="display: flex; background: var(--ats-resume-header); padding: 10px; border-radius: 5px 5px 0 0; justify-content: space-between; border-bottom: 2px solid var(--accent);">
                <div style="color: #ffffff; font-weight: bold; font-size: 12px; display:flex; align-items:center;">
                    📄 Resume Document
                </div>
                <div style="font-size: 12px; color: #ffffff; display:flex; gap: 10px;">
                    <span style="cursor:pointer; color: #ffffff;">🔍 Zoom</span>
                    <span style="cursor:pointer; color: #ffffff;">⬇️ Download</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display the actual PDF if available
        resume_bytes = st.session_state.interview_data.get('resume_bytes')
        
        if resume_bytes:
            # We assume it's a PDF for the viewer (images could be handled too, but PDF is most common)
            base64_pdf = base64.b64encode(resume_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" width="100%" height="80vh" type="application/pdf" style="border:none; border-radius: 0 0 5px 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.3); height: 80vh;"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            # Fallback to Text if no bytes were saved (e.g. legacy session)
            raw_text = st.session_state.interview_data['resume_text']
            formatted_text = raw_text.replace('\n', '<br>')
            st.markdown(f"""
                <div class="ats-resume-container">
                    {formatted_text}
                </div>
            """, unsafe_allow_html=True)
