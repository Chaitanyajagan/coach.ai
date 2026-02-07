import streamlit as st
import time
from streamlit_mic_recorder import mic_recorder
from utils import speak, transcribe_audio_bytes, stop_voice_now

def handle_response(user_text):
    # logic unchanged
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.spinner("Thinking..."):
        ai_data = st.session_state.coach.get_response(
            role=st.session_state.interview_data['role'], 
            user_input=user_text, 
            history=st.session_state.messages[:-1],
            resume_text=st.session_state.interview_data.get('resume_text', "N/A"),
            job_desc=st.session_state.interview_data.get('job_desc', "N/A")
        )
        st.session_state.messages.append({"role": "assistant", "content": ai_data['message']})
        
        # Generate Audio
        from utils import text_to_speech_file
        audio_bytes = text_to_speech_file(ai_data['message'])
        if audio_bytes:
            st.session_state['latest_audio'] = audio_bytes
        
        st.rerun()

def render_interview_view():
    # PLAY AUDIO IF AVAILABLE
    if 'latest_audio' in st.session_state:
        st.audio(st.session_state['latest_audio'], format='audio/wav', autoplay=True)
        # Optional: Delete after playing once to avoid replay on manual refresh? 
        # For now, keep it so it plays on this run. We delete it when new audio comes.
        # del st.session_state['latest_audio']

    # AUTO-START INTERVIEW IF EMPTY
    if not st.session_state.messages:
        with st.spinner("AI Interviewer is preparing the first question..."):
            ai_data = st.session_state.coach.get_response(
                role=st.session_state.interview_data['role'],
                user_input=None, # Start signal
                history=[],
                resume_text=st.session_state.interview_data.get('resume_text', "N/A"),
                job_desc=st.session_state.interview_data.get('job_desc', "N/A")
            )
            st.session_state.messages.append({"role": "assistant", "content": ai_data['message']})
            
            # Generate Audio
            from utils import text_to_speech_file
            audio_bytes = text_to_speech_file(ai_data['message'])
            if audio_bytes:
                st.session_state['latest_audio'] = audio_bytes
            
            st.rerun()

    # We use columns to create the center (feed) and right (stats) panel feel
    col_main, col_right = st.columns([2.5, 1])
    
    with col_main:
        # Header Area
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(f"## {st.session_state.interview_data['role']} Interview")
            st.caption("People attending the call: AI Coach, Candidate (You)")
        
        # Video Container
        with st.container():
             st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
             
             if st.session_state.camera_on:
                 # Camera Input acting as the video feed
                 st.camera_input("Camera Feed", label_visibility="collapsed")
             else:
                 # Static Logo Placeholder
                 st.markdown("""
                 <div style="height: 480px; display: flex; align-items: center; justify-content: center; background: #0a0a0a; border: 1px solid #333; border-radius: 12px;">
                    <img src="https://ui-avatars.com/api/?name=Coach+AI&background=8b5cf6&color=fff&size=200&font-size=0.33&bold=true" style="border-radius: 50%; opacity: 0.9;">
                 </div>
                 """, unsafe_allow_html=True)
             
             # --- CONTROLS ---
             st.markdown("<br>", unsafe_allow_html=True)
             
             # Center the buttons: Spacers on ends, buttons in middle
             # Layout: [Spacer, Btn, Btn, Btn, Btn, Spacer]
             _, c_btn1, c_btn2, c_btn3, c_btn4, _ = st.columns([4, 1, 1, 1, 1, 4])
             
             with st.container():
                 # 1. MIC BUTTON (Browser Native)
                 with c_btn1:
                     audio = mic_recorder(
                        start_prompt="🎙️",
                        stop_prompt="⏹️",
                        just_once=True,
                        use_container_width=False,
                        format="wav",
                        key="mic_recorder"
                     )
                     if audio:
                         st.toast("Processing audio...")
                         user_text = transcribe_audio_bytes(audio['bytes'])
                         if user_text:
                             st.success(f"Heard: {user_text}")
                             time.sleep(0.5)
                             handle_response(user_text)
                         else:
                             st.error("I couldn't understand that. Please try again.")




                 # 2. CAMERA (Toggle)
                 with c_btn2:
                     cam_icon = "📷" if st.session_state.camera_on else "📵"
                     if st.button(cam_icon, help="Toggle Camera"):
                         st.session_state.camera_on = not st.session_state.camera_on
                         st.rerun()

                 # 3. END CALL
                 with c_btn3:
                     if st.button("📞", type="primary", help="End Interview"):
                         # STOP EVERYTHING
                         st.session_state['shutup'] = True
                         stop_voice_now()
                         
                         st.toast("Interview Ended. Calculating Results...")
                         time.sleep(1)
                         st.session_state.dash_view = 'result'
                         st.rerun()
                 
                 # 4. SETTINGS
                 with c_btn4:
                     st.button("⚙️", help="Settings", disabled=True)
             
             # Custom CSS to style these buttons nicely in a row
             st.markdown("""
             <style>
                /* Hide the fake overlay */
                .control-bar-overlay { display: none; }
                
                /* Style the button row to look like a bar */
                div.stButton > button {
                    border-radius: 50% !important;
                    width: 50px !important;
                    height: 50px !important;
                    padding: 0 !important;
                    font-size: 1.5rem !important;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                }
                /* Red Hangup Button */
                div.stButton > button[kind="primary"] {
                    background-color: #ef4444 !important;
                    border-color: #ef4444 !important;
                }
                div.stButton > button[kind="primary"]:hover {
                    background-color: #dc2626 !important;
                }
             </style>
             """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Top Stats
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin-bottom: 20px; text-align: center;">Live Analysis</h4>
            <div style="display: flex; justify-content: space-around;">
                <div class="stat-circle">
                    <div class="stat-inner">
                        <div class="stat-value">80%</div>
                        <div class="stat-label">Video</div>
                    </div>
                </div>
                <div class="stat-circle" style="background: conic-gradient(#f59e0b 0% 65%, #333 65% 100%);">
                    <div class="stat-inner">
                        <div class="stat-value">75%</div>
                        <div class="stat-label">Content</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat / Transcript Panel
        if st.session_state.messages:
            st.markdown('<div class="glass-card" style="max-height: 600px; overflow-y: auto; display: flex; flex-direction: column;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:15px'>Transcript</h4>", unsafe_allow_html=True)
            
            # Transcript Loop (Chronological)
            for msg in st.session_state.messages:
                role_class = "msg-user" if msg['role'] == "user" else "msg-ai"
                icon = "👤" if msg['role'] == "user" else "🤖"
                st.markdown(f"""
                <div class="msg-bubble {role_class}" style="margin-bottom: 10px; padding: 10px; border-radius: 10px; background: rgba(255,255,255,0.05);">
                    <small style="color: #888;">{icon} {msg['role'].title()}</small><br>
                    <span style="color: #fff;">{msg['content']}</span>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
        else:
             st.info("Transcript will appear here.")

    # Handle Text Input (Fallback)
    if prompt := st.chat_input("Type your answer here..."):
        handle_response(prompt)
