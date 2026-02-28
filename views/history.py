import streamlit as st
import database as db
import json
from datetime import datetime

def render_history_view():
    st.markdown("<div class='animate-fade-in delay-1'><h2>📚 Interview History</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Review your past interviews, scores, and detailed transcripts.</p></div>", unsafe_allow_html=True)
    
    uid = st.session_state.get('current_user_id')
    if not uid:
        st.warning("Please log in to view your history.")
        if st.button("⬅ Go to Login"):
            st.session_state.auth_status = False
            st.rerun()
        return

    interviews = db.get_user_interviews(uid)
    
    if not interviews:
        st.info("You haven't completed any interviews yet. Go to Setup to start one!")
        if st.button("🚀 Start New Interview"):
            st.session_state.dash_view = 'setup'
            st.rerun()
        return
        
    st.markdown(f"<div class='animate-fade-in delay-2'><strong>Total Interviews:</strong> {len(interviews)}<hr></div>", unsafe_allow_html=True)
    
    for idx, inv in enumerate(interviews):
        # inv is sqlite3.Row -> id, user_id, role, conversation, final_score, verdict, timestamp
        dt_obj = datetime.strptime(inv['timestamp'], "%Y-%m-%d %H:%M:%S")
        date_str = dt_obj.strftime("%b %d, %Y - %I:%M %p")
        
        score = inv['final_score']
        if score is None:
            score_str = "N/A"
        else:
            # Stored out of 10, display as percent
            score_str = f"{int(float(score) * 10)}%"
            
        role = inv['role']
        stagger = (idx % 4) + 1
        st.markdown(f"<div class='animate-fade-in delay-{stagger}'>", unsafe_allow_html=True)
        with st.expander(f"📌 {role} | 📅 {date_str} | 🏆 Score: {score_str}"):
            # Feedback logic
            verdict_raw = inv['verdict']
            feedback = ""
            if verdict_raw:
                st.markdown("#### Overall Feedback")
                try:
                    v_data = json.loads(verdict_raw)
                    feedback = v_data.get('overall_feedback', str(verdict_raw))
                    if isinstance(feedback, dict):
                        feedback = json.dumps(feedback, indent=2)
                except:
                    feedback = str(verdict_raw)
                st.info(feedback)
                
            # Conversation Transcript
            st.markdown("#### Transcript")
            conv_str = inv['conversation']
            try:
                messages = json.loads(conv_str)
            except:
                messages = []
                
            if messages:
                for msg in messages:
                    if msg['role'] == "user":
                        st.markdown(f"**👤 You:** {msg['content']}")
                    elif msg['role'] == "assistant":
                        st.markdown(f"**🤖 AI Coach:** {msg['content']}")
            else:
                st.write("No transcript available.")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- Generate PDF ---
            try:
                from fpdf import FPDF
                
                class ReportPDF(FPDF):
                    def header(self):
                        self.set_font('Helvetica', 'B', 16)
                        self.set_text_color(0, 51, 102)
                        self.cell(0, 10, 'Coach.ai Interview Report', 0, 1, 'C')
                        self.ln(5)

                    def footer(self):
                        self.set_y(-15)
                        self.set_font('Helvetica', 'I', 8)
                        self.set_text_color(128, 128, 128)
                        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

                pdf = ReportPDF()
                pdf.add_page()
                
                # Title Info
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 8, f"Role: {role}", 0, 1)
                pdf.cell(0, 8, f"Date: {date_str}", 0, 1)
                pdf.cell(0, 8, f"Score: {score_str}", 0, 1)
                pdf.ln(5)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)

                # Feedback
                if feedback:
                    pdf.set_font("Helvetica", "B", 14)
                    pdf.set_text_color(0, 51, 102)
                    pdf.cell(0, 10, "Overall Feedback", 0, 1)
                    pdf.set_font("Helvetica", "", 11)
                    pdf.set_text_color(0, 0, 0)
                    safe_feedback = str(feedback).encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 6, txt=safe_feedback)
                    pdf.ln(5)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(5)

                # Transcript
                pdf.set_font("Helvetica", "B", 14)
                pdf.set_text_color(0, 51, 102)
                pdf.cell(0, 10, "Transcript", 0, 1)
                pdf.ln(2)

                if messages:
                    for msg in messages:
                        is_assistant = msg['role'] == "assistant"
                        if msg['role'] == "user":
                            pdf.set_font("Helvetica", "B", 11)
                            pdf.set_text_color(0, 102, 204)
                            safe_role = "You:"
                        elif is_assistant:
                            pdf.set_font("Helvetica", "B", 11)
                            pdf.set_text_color(0, 153, 76)
                            safe_role = "AI Coach:"
                        else:
                            continue
                            
                        pdf.cell(0, 6, safe_role, 0, 1)
                        if is_assistant:
                            pdf.set_font("Helvetica", "B", 11)  # Bold for questions
                        else:
                            pdf.set_font("Helvetica", "", 11)   # Normal for answers
                        pdf.set_text_color(0, 0, 0)
                        safe_content = msg['content'].encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 6, txt=safe_content)
                        pdf.ln(2)
                        
                        # Add a light line separator
                        pdf.set_draw_color(220, 220, 220) # Light gray
                        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                        pdf.ln(3)
                        pdf.set_draw_color(0, 0, 0) # Reset draw color to black
                else:
                    pdf.set_font("Helvetica", "I", 11)
                    pdf.set_text_color(100, 100, 100)
                    pdf.cell(0, 6, "No transcript available.", 0, 1)

                pdf_bytes = bytes(pdf.output())
            except Exception as e:
                pdf_bytes = str(e).encode('utf-8')
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"Interview_Report_{role.replace(' ', '_')}_{dt_obj.strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key=f"dl_{inv['id']}"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅ Return to Dashboard"):
        st.session_state.dash_view = 'setup'
        st.rerun()
