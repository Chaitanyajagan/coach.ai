import streamlit as st
import time
from streamlit_mic_recorder import mic_recorder
from utils import speak, transcribe_audio_bytes, stop_voice_now
import database as db

def handle_response(user_text):
    # logic unchanged
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    # Inject closing prompt on 5th user answer (10th total message since it alternates)
    prompt_modifier = user_text
    if len(st.session_state.messages) >= 10:
        prompt_modifier += "\n\n[SYSTEM: This is the 5th and final answer. You MUST evaluate the entire interview, provide a final score and verdict, and set status to 'finished'. Do NOT ask any more questions.]"
        
    with st.spinner("Thinking..."):
        ai_data = st.session_state.coach.get_response(
            role=st.session_state.interview_data['role'], 
            user_input=prompt_modifier, 
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
        
        # Update Score if present
        if ai_data.get('score'):
            try:
                # stored as 0-10, display as % by multiplying by 10 later
                st.session_state.current_score = float(ai_data['score']) 
            except:
                pass

        # Check for Interview Completion
        if ai_data.get('final_score'):
            st.session_state.interview_data['final_score'] = ai_data['final_score']
        
        if ai_data.get('verdict'):
            st.session_state.interview_data['verdict'] = ai_data['verdict']
        
        if ai_data.get('status') == 'finished':
            # Save to Database before routing to results
            uid = st.session_state.get('current_user_id')
            if uid:
                import json
                # final_score and verdict might be in interview_data now
                f_score = st.session_state.interview_data.get('final_score')
                verdict_str = st.session_state.interview_data.get('verdict')
                if isinstance(verdict_str, dict):
                    verdict_str = json.dumps(verdict_str)
                    
                db.save_interview(
                    user_id=uid,
                    role=st.session_state.interview_data.get('role', 'Unknown Role'),
                    messages=st.session_state.messages,
                    final_score=f_score,
                    verdict=verdict_str
                )
            
            st.toast("Interview Completed! Generating Results...")
            time.sleep(2)
            st.session_state.dash_view = 'result'
            st.rerun()
            
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
            st.markdown(f"<div class='animate-fade-in delay-1'><h2>{st.session_state.interview_data['role']} Interview</h2></div>", unsafe_allow_html=True)
            st.caption("People attending the call: AI Coach, Candidate (You)")
        
        # Video Container
        with st.container():
             st.markdown('<div class="video-wrapper animate-fade-in delay-2">', unsafe_allow_html=True)
             
             if st.session_state.camera_on:
                 # Camera Input acting as the video feed
                 st.camera_input("Camera Feed", label_visibility="collapsed")
             else:
                 # Static Logo Placeholder
                 st.markdown("""
                 <div style="height: 480px; display: flex; align-items: center; justify-content: center; background: var(--video-bg); border: 1px solid var(--video-border); border-radius: 12px;">
                    <img src="https://ui-avatars.com/api/?name=Coach+AI&background=1e3a8a&color=fff&size=200&font-size=0.33&bold=true" style="border-radius: 50%; opacity: 0.9;">
                 </div>
                 """, unsafe_allow_html=True)
             
             # --- CONTROLS ---
             # --- CONTROLS ---
             import base64
             import os
             
             def get_base64_svg(file_path):
                 if os.path.exists(file_path):
                     with open(file_path, "rb") as f:
                         return base64.b64encode(f.read()).decode()
                 return ""

             # Load local SVGs
             icons_dir = "c:/coach.ai(1)/static/icons"
             mic_on_b64 = get_base64_svg(f"{icons_dir}/mic-on.svg")
             mic_off_b64 = get_base64_svg(f"{icons_dir}/mic-off.svg")
             video_on_b64 = get_base64_svg(f"{icons_dir}/video-on.svg")
             video_off_b64 = get_base64_svg(f"{icons_dir}/video-off.svg")
             phone_off_b64 = get_base64_svg(f"{icons_dir}/phone-off.svg")
             
             st.markdown("<br>", unsafe_allow_html=True)
             
             # Center the buttons: Mic, Camera, and End Call
             _, c_btn1, c_btn2, c_btn3, _ = st.columns([3.5, 1, 1, 1, 3.5])
             
             with st.container():
                 st.markdown('<div id="interview-controls-marker" style="display:none"></div>', unsafe_allow_html=True)
                 
                 # 1. MIC BUTTON (Relies on streamlit_mic_recorder iframe)
                 with c_btn1:
                     st.markdown('<span id="mic-btn-wrapper" style="display:none;"></span>', unsafe_allow_html=True)
                     
                     audio = mic_recorder(
                        start_prompt="MIC_OFF",
                        stop_prompt="MIC_ON",
                        just_once=True,
                        use_container_width=True,
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

                 # 2. CAMERA BUTTON (Toggle)
                 with c_btn2:
                     is_cam_on = st.session_state.camera_on
                     cam_id = f"camera-btn-{is_cam_on}"
                     st.markdown(f'<span id="{cam_id}" style="display:none;"></span>', unsafe_allow_html=True)
                     if st.button(" ", help="Toggle Camera", use_container_width=True, key="cam_toggle_btn"):
                         st.session_state.camera_on = not st.session_state.camera_on
                         st.rerun()

                 # 3. END CALL BUTTON
                 with c_btn3:
                     st.markdown('<span id="end-call-btn" style="display:none;"></span>', unsafe_allow_html=True)
                     if st.button(" ", help="End Interview", use_container_width=True, key="end_call_btn"):
                         st.session_state['shutup'] = True
                         stop_voice_now()
                         st.toast("Interview Ended. Calculating Results...")
                         time.sleep(1)
                         st.session_state.dash_view = 'result'
                         st.rerun()

             # Custom CSS to apply the SVGs to the Native Streamlit Buttons
             st.markdown(f"""
             <style>
             /* General Button Resizing for control buttons */
             div[data-testid="stHorizontalBlock"]:has(#interview-controls-marker) button {{
                 height: 55px !important;
                 border-radius: 14px !important;
                 transition: all 0.2s ease !important;
                 border: 1px solid var(--border-color) !important;
             }}
             
             /* Camera Button states */
             div.element-container:has(#camera-btn-True) + div.element-container button {{
                 background: var(--card-bg) url('data:image/svg+xml;base64,{video_on_b64}') no-repeat center center / 24px 24px !important;
             }}
             div.element-container:has(#camera-btn-False) + div.element-container button {{
                 background: var(--card-bg) url('data:image/svg+xml;base64,{video_off_b64}') no-repeat center center / 24px 24px !important;
             }}
             
             /* End Call Button */
             div.element-container:has(#end-call-btn) + div.element-container button {{
                 background: #ef4444 url('data:image/svg+xml;base64,{phone_off_b64}') no-repeat center center / 24px 24px !important;
                 border: 1px solid #dc2626 !important;
             }}
             div.element-container:has(#end-call-btn) + div.element-container button:hover {{
                 background-color: #dc2626 !important;
                 transform: scale(1.05);
             }}
             
             /* Dark Theme Icon Inversions for Camera using brightness/invert filters to make black SVGs white */
             [data-custom-theme="dark"] div.element-container:has(#camera-btn-True) + div.element-container button,
             [data-custom-theme="dark"] div.element-container:has(#camera-btn-False) + div.element-container button {{
                 filter: invert(1) brightness(2);
             }}
             /* Re-invert End Call because we forced it to be red! */
             [data-custom-theme="dark"] div.element-container:has(#end-call-btn) + div.element-container button {{
                 filter: none;
             }}
             
             /* Remove textual content */
             div[data-testid="stHorizontalBlock"]:has(#interview-controls-marker) button p {{
                 display: none !important;
             }}
             
             /* Style microphone iframe row generically so it sits cleanly */
             div[data-testid="column"]:nth-child(2) iframe {{
                 border-radius: 14px !important;
                 border: 1px solid var(--border-color) !important;
             }}
             
             /* Pure CSS Mic Button Overlay Trick Setup */
             div.element-container:has(#mic-btn-wrapper) + div.element-container {{
                 position: relative;
                 background: var(--card-bg) url('data:image/svg+xml;base64,{mic_off_b64}') no-repeat center center / 24px 24px !important;
                 border-radius: 14px !important;
                 border: 1px solid var(--border-color) !important;
                 overflow: hidden;
                 min-height: 55px !important;
                 display: flex;
                 align-items: center;
                 justify-content: center;
                 transition: all 0.2s ease;
             }}
             
             /* When clicked and recording, change the icon to mic-on using focus-within! */
             div.element-container:has(#mic-btn-wrapper) + div.element-container:focus-within {{
                 background-image: url('data:image/svg+xml;base64,{mic_on_b64}') !important;
                 border-color: #ef4444 !important; /* Red border to indicate recording */
             }}
             
             /* Dark Theme for the Mic Overlay */
             [data-custom-theme="dark"] div.element-container:has(#mic-btn-wrapper) + div.element-container {{
                 filter: invert(1) brightness(2);
             }}
             /* Don't invert the red border when active in dark mode */
             [data-custom-theme="dark"] div.element-container:has(#mic-btn-wrapper) + div.element-container:focus-within {{
                 filter: none;
                 background-color: #374151 !important;
             }}
             
             /* Make the actual Streamlit iframe invisible but fully clickable and positioned over our visual overlay */
             div.element-container:has(#mic-btn-wrapper) + div.element-container iframe {{
                 opacity: 0.001 !important;
                 position: absolute;
                 z-index: 10;
                 min-height: 55px !important;
                 width: 100% !important;
                 /* Slightly scale out to hide internal borders and ensure full hit area */
                 transform: scale(1.05);
             }}
             </style>
             """, unsafe_allow_html=True)

    with col_right:
        # Top Stats
        # Calculate stats for cleaner f-string
        score_val = int(st.session_state.current_score * 10)
        ques_count = len(st.session_state.messages)//2
        ques_pct = int((ques_count / 5) * 100)
        
        st.markdown(f"""
<div class="glass-card animate-fade-in delay-3">
    <h4 style="margin-bottom: 20px; text-align: center;">Live Analysis</h4>
    <div style="display: flex; justify-content: space-around;">
        <div class="stat-circle" style="background: conic-gradient(var(--accent) 0% {score_val}%, var(--circle-bg) {score_val}% 100%);">
            <div class="stat-inner">
                <div class="stat-value">{score_val}%</div>
                <div class="stat-label">Score</div>
            </div>
        </div>
        <div class="stat-circle" style="background: conic-gradient(#f59e0b 0% {ques_pct}%, var(--circle-bg) {ques_pct}% 100%);">
            <div class="stat-inner">
                <div class="stat-value">{ques_count}/5</div>
                <div class="stat-label">Ques</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # Chat / Transcript Panel
        if st.session_state.messages:
            # Build the transcript HTML as a single string to ensure structural integrity
            # Build the transcript HTML as a single string to ensure structural integrity
            # Outer Card
            transcript_html = '<div class="glass-card animate-fade-in delay-4">'
            # Fixed Header
            transcript_html += "<h4 style='margin-bottom:15px'>Transcript</h4>"
            
            # Scrollable Body Container
            transcript_html += '<div class="transcript-body">'
            
            for msg in st.session_state.messages:
                role_class = "msg-user" if msg['role'] == "user" else "msg-ai"
                icon = "👤" if msg['role'] == "user" else "🤖"
                # Use single line strings to avoid markdown code block interpretation (indentation)
                transcript_html += f'<div class="msg-bubble {role_class} animate-fade-in">'
                transcript_html += f'<small style="color: var(--text-secondary);">{icon} {msg["role"].title()}</small><br>'
                transcript_html += f'<span style="color: var(--text-primary);">{msg["content"]}</span>'
                transcript_html += '</div>'
            
            transcript_html += '</div></div>' # Close body, then card
            st.markdown(transcript_html, unsafe_allow_html=True)
        else:
             st.info("Transcript will appear here.")

    # Handle Text Input (Fallback)
    if prompt := st.chat_input("Type your answer here..."):
        handle_response(prompt)
