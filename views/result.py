import streamlit as st
from textwrap import dedent

import re
def render_html(html_str):
    st.markdown(re.sub(r'^[ 	]+', '', html_str, flags=re.MULTILINE), unsafe_allow_html=True)

def render_result_view():
    # Inject Custom Dashboard CSS
    render_html("""
        <style>
        /* Base Variables specific to Dashboard */
        :root {
            --wonsult-bg: #f9fafb;
            --wonsult-card: #ffffff;
            --wonsult-text-main: #1f2937;
            --wonsult-text-sub: #6b7280;
            --wonsult-primary: #2d8174; /* teal button */
            --wonsult-border: #e5e7eb;
            --wonsult-ring: #0f766e; /* dark teal circle ring */
        }
        
        /* Dark mode overrides (optional fallbacks if user is in dark mode, but trying to keep true to the light theme image) */
        [data-custom-theme="dark"] {
            --wonsult-bg: #111827;
            --wonsult-card: #1f2937;
            --wonsult-text-main: #f9fafb;
            --wonsult-text-sub: #9ca3af;
            --wonsult-border: #374151;
        }

        /* Card Setup */
        .dash-card {
            background-color: var(--wonsult-card);
            border: 1px solid var(--wonsult-border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        
        .card-header-sub {
            font-size: 11px;
            font-weight: bold;
            color: var(--wonsult-text-sub);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--wonsult-text-main);
            margin-bottom: 20px;
        }
        
        .card-meta {
            font-size: 13px;
            color: var(--wonsult-text-sub);
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .dash-btn {
            background-color: var(--wonsult-primary);
            color: white !important;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 12px;
            cursor: pointer;
            text-align: center;
            display: inline-block;
            transition: background 0.2s;
        }
        .dash-btn:hover {
            background-color: #236c61;
        }
        
        .dash-btn-outline {
            background-color: transparent;
            color: var(--wonsult-primary) !important;
            border: 1px solid var(--wonsult-primary);
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 12px;
            cursor: pointer;
            text-align: center;
            display: inline-block;
        }
        
        /* Stats Row */
        .stats-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .stats-number {
            font-size: 28px;
            font-weight: 700;
            color: var(--wonsult-primary);
            margin-right: 15px;
        }
        .stats-text {
            font-size: 15px;
            font-weight: 600;
            color: var(--wonsult-text-main);
        }

        /* Progress Chart Mock */
        .chart-container {
            height: 250px;
            display: flex;
            align-items: flex-end;
            gap: 40px;
            padding-top: 40px;
            padding-left: 20px;
            border-bottom: 1px solid var(--wonsult-border);
            border-left: 1px solid var(--wonsult-border);
            margin-top: 20px;
            position: relative;
        }
        
        /* Tooltip style */
        .chart-tooltip {
            position: absolute;
            top: 40px;
            left: 55%;
            background: #374151;
            color: white;
            padding: 10px;
            border-radius: 6px;
            font-size: 11px;
            line-height: 1.5;
            z-index: 10;
        }
        
        /* Y-Axis Grid Lines */
        .y-axis-grid {
            position: absolute;
            top: 40px;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            pointer-events: none;
            z-index: 0;
        }
        .y-tick {
            width: 100%;
            height: 1px;
            background-color: var(--wonsult-border);
            opacity: 0.5; /* soft line */
            position: relative;
        }
        .y-tick:last-child {
            background-color: transparent; /* hide bottom line, overlaps x-axis */
        }
        .y-label {
            position: absolute;
            left: -35px;
            top: -5px; /* nicely center 10px text horizontally with 1px line */
            font-size: 10px;
            color: var(--wonsult-text-sub);
            width: 25px;
            text-align: right;
            line-height: 1;
        }
        
        .bar-group {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            height: 100%;
            width: 30px;
            position: relative;
            z-index: 1;
        }
        
        .bar-segment { width: 100%; }
        .b-top { background-color: #3b82f6; border-top-left-radius: 3px; border-top-right-radius: 3px; }
        .b-mid { background-color: #10b981; }
        .b-bot { background-color: #f59e0b; }
        
        .bar-label {
            position: absolute;
            bottom: -25px;
            font-size: 10px;
            color: var(--wonsult-text-sub);
            white-space: nowrap;
        }

        /* Right Panel Widgets */
        .score-circle-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px 0;
        }
        .score-ring {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            /* dynamic background applied inline */
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .score-inner {
            width: 80px;
            height: 80px;
            background-color: var(--wonsult-card);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 700;
            color: var(--wonsult-primary);
            position: absolute;
            z-index: 2;
        }
        
        .score-title {
            font-size: 12px;
            font-weight: 700;
            color: var(--wonsult-primary);
        }

        .breakdown-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 12px;
        }
        .breakdown-label {
            color: var(--wonsult-text-main);
            width: 100px;
            font-weight: 500;
        }
        .breakdown-pct {
            flex-grow: 1;
            text-align: right;
            padding-right: 15px;
        }
        .breakdown-bar-container {
            width: 60px;
            height: 4px;
            background: var(--wonsult-border);
            border-radius: 2px;
            overflow: hidden;
        }
        .breakdown-bar {
            height: 100%;
            border-radius: 2px;
        }
        .pct-content { color: #3b82f6; font-weight: 600; }
        .bg-content { background: #3b82f6; }
        .pct-speech { color: #10b981; font-weight: 600; }
        .bg-speech { background: #10b981; }
        .pct-facial { color: #f59e0b; font-weight: 600; }
        .bg-facial { background: #f59e0b; }

        .feedback-text {
            font-size: 12px;
            line-height: 1.6;
            color: var(--wonsult-text-main);
        }
        </style>
    """)
    
    import json
    from database import get_user_interviews
    
    # Check for user_id in session_state, fetch interviews
    user_id = st.session_state.get('current_user_id')
    interviews = get_user_interviews(user_id) if user_id else []
    
    num_interviews = len(interviews)
    
    total_score = 0
    total_content = 0
    total_speech = 0
    total_facial = 0
    valid_scores_count = 0
    feedback_text = ""
    
    progress_bars_html = ""
    recent_cards_html = ""
    
    if num_interviews == 0:
        avg_score_100 = 0
        avg_content = 0
        avg_speech = 0
        avg_facial = 0
        feedback_text = "No interviews completed yet. Start an interview to see your feedback."
        
        recent_cards_html = """
            <div style="display:flex; gap: 20px; width: 100%;">
                <div class="dash-card" style="flex:1;">
                    <div class="card-header-sub">MOST RECENT</div>
                    <div class="card-title">No Recent Interviews</div>
                    <div class="card-meta">
                        <span>🕒 0 min</span>
                        <span>💬 0 questions</span>
                    </div>
                </div>
                <div class="dash-card" style="flex:1;">
                    <div class="card-header-sub">MOST RECENT</div>
                    <div class="card-title">No Recent Interviews</div>
                    <div class="card-meta">
                        <span>🕒 0 min</span>
                        <span>💬 0 questions</span>
                    </div>
                </div>
            </div>
        """
        
        progress_bars_html = f"""
            <div class="bar-group" style="margin-left:20px;">
                <div class="bar-segment b-top" style="height: 0%;"></div>
                <div class="bar-segment b-mid" style="height: 0%;"></div>
                <div class="bar-segment b-bot" style="height: 0%;"></div>
                <div class="bar-label">No Data</div>
            </div>
        """
    else:
        # Take the most recent 4 interviews and reverse them for chronological rendering
        recent_four = list(reversed(interviews[:4]))
        
        cards = []
        for inv in interviews[:2]:
            try:
                # Load JSON conversation to count messages correctly
                msg_dict = json.loads(inv['conversation']) if inv['conversation'] else []
                msg_count = len([m for m in msg_dict if m.get('role') == 'user']) if isinstance(msg_dict, list) else 0
            except:
                msg_count = 0
                
            role = inv['role'] if inv['role'] else "Interview"
            dt_str = inv['timestamp'].split(' ')[0] if inv['timestamp'] else ""
            cards.append(f"""
                <div class="dash-card" style="flex:1;">
                    <div class="card-header-sub">MOST RECENT</div>
                    <div class="card-title">{role}</div>
                    <div class="card-meta">
                        <span>� {dt_str}</span>
                        <span>💬 {msg_count} responses</span>
                    </div>
                </div>
            """)
            
        if len(cards) == 1:
            cards.append(f"""
                <div class="dash-card" style="flex:1;">
                    <div class="card-header-sub">MOST RECENT</div>
                    <div class="card-title">No Recent Interviews</div>
                    <div class="card-meta">
                        <span>🕒 0 min</span>
                        <span>💬 0 questions</span>
                    </div>
                </div>
            """)
            
        recent_cards_html = f"""<div style="display:flex; gap: 20px; width: 100%; margin-bottom: 20px;">{"".join(cards)}</div>"""
        
        for inv in interviews:
            score_raw = inv['final_score']
            s_100 = int(float(score_raw) * 10) if score_raw is not None else 0
            
            raw_verdict = inv['verdict'] or '{}'
            if isinstance(raw_verdict, str):
                try:
                    verdict_data = json.loads(raw_verdict)
                except:
                    verdict_data = {"overall_feedback": str(raw_verdict)}
            else:
                verdict_data = raw_verdict
                
            if valid_scores_count == 0:
                if isinstance(verdict_data, dict) and 'overall_feedback' in verdict_data:
                    feedback_text = verdict_data['overall_feedback']
            
            c_score = min(100, s_100 + 5)
            sp_score = max(0, s_100 - 10)
            f_score = max(0, s_100 - 15)
            
            total_score += s_100
            total_content += c_score
            total_speech += sp_score
            total_facial += f_score
            valid_scores_count += 1
            
        if not feedback_text:
            feedback_text = "Good effort on your interviews. Keep practicing to improve your scores."
            
        avg_score_100 = int(total_score / valid_scores_count) if valid_scores_count else 0
        avg_content = int(total_content / valid_scores_count) if valid_scores_count else 0
        avg_speech = int(total_speech / valid_scores_count) if valid_scores_count else 0
        avg_facial = int(total_facial / valid_scores_count) if valid_scores_count else 0
        
        for i, inv in enumerate(recent_four):
            score_raw = inv['final_score']
            s_100 = int(float(score_raw) * 10) if score_raw is not None else 0
            
            c_score = min(100, s_100 + 5)
            sp_score = max(0, s_100 - 10)
            f_score = max(0, s_100 - 15)
            
            # Scale down bar heights to fit relatively
            h_c = c_score * 0.33
            h_s = sp_score * 0.33
            h_f = f_score * 0.33
            
            try:
                # Format MM-DD
                dt_str = inv['timestamp'].split(' ')[0][5:] if inv['timestamp'] else "Date"
            except:
                dt_str = "Date"
            
            progress_bars_html += f"""
                <div class="bar-group" {"style='margin-left:20px;'" if i==0 else ""}>
                    <div class="bar-segment b-top" style="height: {h_c}%;"></div>
                    <div class="bar-segment b-mid" style="height: {h_s}%;"></div>
                    <div class="bar-segment b-bot" style="height: {h_f}%;"></div>
                    <div class="bar-label">{dt_str}</div>
                </div>
            """

    # Layout: Main Area (Left) and Right Sidebar
    col_main, col_side = st.columns([1.8, 1])

    with col_main:
        render_html(recent_cards_html)
            
        # Stats Bar Row
        render_html(f"""
            <div class="dash-card stats-bar">
                <div style="display:flex; align-items:center;">
                    <span class="stats-number">{num_interviews}</span>
                    <span class="stats-text">Interviews Completed</span>
                </div>
            </div>
        """)

        # Progress Chart Card
        render_html(f"""
            <div class="dash-card">
                <div style="display:flex; justify-content:space-between;">
                    <h3 style="margin:0; font-size:18px; color:var(--wonsult-text-main);">Your Progress</h3>
                    <div style="font-size:9px; color:var(--wonsult-text-sub); line-height:1.6; text-align:right;">
                        <span style="display:inline-block; width:8px; height:8px; background:#3b82f6; margin-right:4px;"></span>Content<br>
                        <span style="display:inline-block; width:8px; height:8px; background:#10b981; margin-right:4px;"></span>Speech<br>
                        <span style="display:inline-block; width:8px; height:8px; background:#f59e0b; margin-right:4px;"></span>Facial Emotions
                    </div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-tooltip">
                        Averages from recent activity
                    </div>
                    
                    <!-- Y-Axis Grid Lines -->
                    <div class="y-axis-grid">
                        <div class="y-tick"><div class="y-label">100</div></div>
                        <div class="y-tick"><div class="y-label">75</div></div>
                        <div class="y-tick"><div class="y-label">50</div></div>
                        <div class="y-tick"><div class="y-label">25</div></div>
                        <div class="y-tick"><div class="y-label">0</div></div>
                    </div>
                    
                    {progress_bars_html}
                </div>
            </div>
        """)

    with col_side:
        # Right Side - Average Score
        render_html(f"""
            <div class="dash-card score-circle-wrapper">
                <div class="score-ring" style="background: conic-gradient(var(--wonsult-primary) {avg_score_100}%, var(--wonsult-border) 0); margin-bottom: 15px;">
                    <div class="score-inner">{avg_score_100}</div>
                </div>
                <div class="score-title">Average Interview Score</div>
            </div>
        """)

        # Right Side - Breakdown
        render_html(f"""
            <div class="dash-card">
                <div style="text-align:center; font-size:12px; font-weight:700; color:var(--wonsult-primary); margin-bottom: 20px;">Score Breakdown Averages</div>
                
                <div class="breakdown-row">
                    <div class="breakdown-label">Content</div>
                    <div class="breakdown-pct pct-content">{avg_content}%</div>
                </div>
                
                <div class="breakdown-row">
                    <div class="breakdown-label">Speech</div>
                    <div class="breakdown-pct pct-speech">{avg_speech}%</div>
                </div>
                
                <div class="breakdown-row">
                    <div class="breakdown-label">Facial Emotions</div>
                    <div class="breakdown-pct pct-facial">{avg_facial}%</div>
                </div>
            </div>
        """)

        # Right Side - Feedback
        render_html(f"""
            <div class="dash-card">
                <div style="text-align:center; font-size:12px; font-weight:700; color:var(--wonsult-primary); margin-bottom: 15px;">Most Recent Feedback</div>
                <div class="feedback-text">
                    {feedback_text}
                </div>
            </div>
        """)

    # Navigation Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅ Return to Dashboard", use_container_width=True):
            st.session_state.dash_view = 'setup'
            st.rerun()
    with c2:
        if st.button("📚 View Full History", type="primary", use_container_width=True):
            st.session_state.dash_view = 'history'
            st.rerun()
