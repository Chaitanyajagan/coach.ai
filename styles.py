import streamlit.components.v1 as components
import os

def load_local_css(file_name):
    # Search relative to styles.py
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "static", "css", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_local_js(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "static", "js", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f"<script>{f.read()}</script>"
    except FileNotFoundError:
        return ""

def get_global_styles():
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@400;600;700&display=swap');
    
    :root {
        --bg-color: #000000; /* Deep black for dark theme */
        --bg-image: 
            radial-gradient(ellipse at center, rgba(30, 30, 30, 0.8) 0%, transparent 70%),
            repeating-linear-gradient(45deg, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 2px, transparent 2px, transparent 12px),
            repeating-linear-gradient(-45deg, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 2px, transparent 2px, transparent 12px),
            radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
        --bg-size: 100% 100%, 350px 100%, 350px 100%, 14px 14px;
        --bg-position: center, left top, right top, center;
        --bg-repeat: no-repeat, no-repeat, no-repeat, repeat;
        --card-bg: rgba(25, 25, 25, 0.6);
        --accent: #8b5cf6;
        --text-primary: #e5e5e5;
        --text-secondary: #a3a3a3;
        --border-color: rgba(255, 255, 255, 0.1);
        --font-heading: 'Outfit', sans-serif;
        --font-body: 'Inter', sans-serif;
        --video-bg: #000;
        --video-border: #333;
        --stat-inner: #1e1e1e;
        --circle-bg: #333;
        --msg-bg: rgba(255,255,255,0.05);
        --btn-bg-1: #2a2a2a;
        --btn-bg-2: #1a1a1a;
        --btn-text: #ffffff;
        --btn-hover-text: #ffffff;
        --input-bg: rgba(255, 255, 255, 0.05);
        --heading-color: #ffffff;
        
        /* ATS Score View Colors (Dark Theme) */
        --ats-card-bg: #1E1E1E;
        --ats-border: #333333;
        --ats-text-primary: #FFFFFF;
        --ats-text-secondary: #aaaaaa;
        --ats-circle-bg: #111111;
        --ats-resume-bg: #1a1a2e;
        --ats-resume-header: #3f51b5;
        --ats-resume-header-text: #ffffff;
        --ats-resume-text: #FFFFFF;
        --ats-recommendation-number: #333333;
        --ats-recommendation-number-text: #FFFFFF;
        --ats-highlight-green: #2e7d32;
        --ats-highlight-orange: #f57c00;
        --ats-highlight-red: #c62828;
        --ats-highlight-text: #ffffff;
    }
    
    [data-custom-theme="light"] {
        --bg-color: #F8FAFC; /* Slate background */
        --bg-image: 
            radial-gradient(ellipse at center, rgba(255,255,255,1) 0%, rgba(248,250,252,0) 70%),
            repeating-linear-gradient(45deg, rgba(148,163,184,0.1) 0px, rgba(148,163,184,0.1) 2px, transparent 2px, transparent 12px),
            repeating-linear-gradient(-45deg, rgba(148,163,184,0.1) 0px, rgba(148,163,184,0.1) 2px, transparent 2px, transparent 12px),
            radial-gradient(circle, rgba(148,163,184,0.15) 1px, transparent 1px);
        --bg-size: 100% 100%, 350px 100%, 350px 100%, 14px 14px;
        --bg-position: center, left top, right top, center;
        --bg-repeat: no-repeat, no-repeat, no-repeat, repeat;
        --card-bg: #FFFFFF; /* White boxes */
        --accent: #7C3AED; /* Accent hover */
        --text-primary: #0F172A; /* Dark Slate text */
        --text-secondary: #475569; /* Secondary Slate text */
        --border-color: #94A3B8; /* Slate Borders (Darker for visibility) */
        --video-bg: #FFFFFF;
        --video-border: #94A3B8;
        --stat-inner: #FFFFFF;
        --circle-bg: #CBD5E1;
        --msg-bg: #FFFFFF;
        --btn-bg-1: #2563EB; /* Blue to Purple gradient start */
        --btn-bg-2: #7C3AED; /* Purple gradient end */
        --btn-border: #2563EB; /* Default Border */
        --btn-text: #FFFFFF !important; /* White text on Button */
        --btn-hover-text: #FFFFFF !important; 
        --input-bg: #F1F5F9; /* Dropbox background */
        --heading-color: #0F172A; /* Dark Slate headings */
        
        /* ATS Score View Colors (Light Theme) */
        --ats-card-bg: #FFFFFF;
        --ats-border: #e0e0e0;
        --ats-text-primary: #333333;
        --ats-text-secondary: #666666;
        --ats-circle-bg: #FFFFFF;
        --ats-resume-bg: #FAFAFA;
        --ats-resume-header: #3f51b5;
        --ats-resume-header-text: #ffffff;
        --ats-resume-text: #111111;
        --ats-recommendation-number: #f5f5f5;
        --ats-recommendation-number-text: #555555;
        --ats-highlight-green: #e8f5e9;
        --ats-highlight-orange: #fff3e0;
        --ats-highlight-red: #ffebee;
        --ats-highlight-text: #000000;
    }
    
    .stApp {
        background-color: var(--bg-color) !important; 
        background-image: var(--bg-image) !important;
        background-size: var(--bg-size) !important;
        background-position: var(--bg-position) !important;
        background-repeat: var(--bg-repeat) !important;
        background-attachment: fixed !important;
        color: var(--text-primary) !important;
    }
    
    html, body, [class*="css"] {
        font-family: var(--font-body);
        color: var(--text-primary);
    }
    
    /* Override Streamlit's default typography colors */
    p, span, div, label {
        color: var(--text-primary);
    }
    
    /* Override headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        font-weight: 600;
        color: var(--heading-color) !important;
    }
    
    /* Target Sidebar explicitly to fix visibility */
    [data-testid="stSidebar"] {
        background-color: var(--bg-color) !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--heading-color) !important;
    }
    
    /* Force Streamlit Alert/Info boxes to respect theme color */
    [data-testid="stAlert"] * {
        color: var(--text-primary) !important;
    }
    
    /* SCROLLBAR STYLING */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--msg-bg);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 4px;
        opacity: 0.8;
    }
    
    /* TRANSCRIPT CONTAINER */
    .transcript-body {
        height: 400px; 
        overflow-y: auto; 
        display: flex; 
        flex-direction: column;
        padding-right: 10px;
    }
    
    .msg-bubble {
        word-wrap: break-word;
        overflow-wrap: break-word;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        background: var(--msg-bg);
    }

    /* Glassmorphism Card Utils */
    .glass-card {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        border-color: var(--accent) !important;
    }

    /* Video Container */
    .video-wrapper {
        position: relative; 
        border-radius: 16px; 
        overflow: hidden; 
        background: var(--video-bg);
        border: 1px solid var(--video-border);
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    
    /* Stats Circular Progress */
    .stat-circle {
        position: relative;
        width: 80px; 
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stat-inner {
        width: 65px; 
        height: 65px; 
        background: var(--stat-inner); 
        border-radius: 50%;
        display: flex; 
        flex-direction: column;
        align-items: center; 
        justify-content: center;
    }
    .stat-value { font-weight: bold; font-size: 1.1rem; color: var(--text-primary); }
    .stat-label { font-size: 0.6rem; color: var(--text-secondary); text-transform: uppercase; }

    /* Custom Button Styling for standard and form buttons */
    div.stButton > button, 
    div[data-testid="stFormSubmitButton"] > button,
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, var(--btn-bg-1), var(--btn-bg-2)) !important;
        color: var(--btn-text) !important;
        background-color: var(--btn-bg-1) !important;
        border: 1px solid var(--btn-border, #1a1a1a) !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    /* Explicitly ensure the inner paragraph tag inside the button inherits the right color */
    div.stButton > button p, 
    div[data-testid="stFormSubmitButton"] > button p,
    button[data-testid="baseButton-secondary"] p {
        color: var(--btn-text) !important;
    }

    div.stButton > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background: var(--accent) !important;
        color: var(--btn-hover-text) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 15px rgba(109, 40, 217, 0.4);
    }
    
    div.stButton > button:hover p, 
    div[data-testid="stFormSubmitButton"] > button:hover p,
    button[data-testid="baseButton-secondary"]:hover p {
        color: var(--btn-hover-text) !important;
    }
    
    /* Inputs and Dropdowns Fix */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="popover"],
    div[data-testid="stPopoverBody"],
    ul[data-testid="stDropDownMenu"],
    ul[role="listbox"],
    li[role="option"] {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px;
    }
    
    /* Ensure all text inside the select dropdowns, popovers, and menus are the correct color */
    div[data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[data-testid="stPopoverBody"] *,
    div[role="menu"] *,
    div[role="listbox"] *,
    ul[data-testid="stDropDownMenu"] *,
    [data-baseweb="menu"] *,
    [role="menuitem"] span,
    .st-emotion-cache-1vt4ygl * /* Direct hit on typical Streamlit 1.x dropdown class */ {
        color: var(--text-primary) !important;
    }

    /* Aggressive Override Streamlit Top-Right Settings Menu and any Portal Backgrounds */
    ul[data-testid="stDropDownMenu"],
    div[data-testid="stPopoverBody"],
    [data-baseweb="menu"],
    div[role="menu"],
    div[data-baseweb="popover"] > div,
    .st-emotion-cache-1vt4ygl {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Tooltip / Hover Help Text Fix */
    div[data-baseweb="tooltip"],
    div[data-testid="stTooltipContent"],
    div[data-testid="stTooltipContent"] * {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }

    /* Form Boxes Container styling */
    [data-testid="stForm"] {
        background-color: var(--card-bg) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 30px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Streamlit Modal/Dialog Window Fix */
    div[role="dialog"],
    [data-testid="stDialog"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
    }
    div[role="dialog"] *,
    [data-testid="stDialog"] * {
        color: var(--text-primary) !important;
    }

    /* File Uploader Aggressive Form Fix */
    [data-testid="stFileUploader"] > section,
    [data-testid="stFileUploader"] > div {
        background-color: var(--input-bg) !important;
        border: 2px dashed var(--border-color) !important;
    }
    
    /* Target everything inside the file uploader dropzone to force text color */
    [data-testid="stFileUploader"] *,
    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploadDropzone"] * {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stFileUploadDropzone"] {
        background-color: var(--input-bg) !important;
    }
    
    /* Fix 'Browse files' button inside Uploader */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, var(--btn-bg-1), var(--btn-bg-2)) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        font-weight: 600;
    }

    /* Checkbox text */
    .stCheckbox > label {
        color: var(--text-primary) !important;
    }

    /* Streamlit Toast Notification Fix */
    [data-testid="stToast"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        border-radius: 8px !important;
    }
    [data-testid="stToast"] * {
        color: var(--text-primary) !important;
    }
    [data-custom-theme="dark"] [data-testid="stToast"] {
        background-color: #1e2432 !important;
        border-color: #353e54 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }
    [data-custom-theme="dark"] [data-testid="stToast"] * {
        color: #e1e9f5 !important;
    }

""" + "\n" + load_local_css("animations.css") + "\n" + load_local_css("components.css") + "\n</style>\n"

def inject_theme_toggle():
    components.html("""
    <script>
        const parentDoc = window.parent.document;
        
        let container = parentDoc.getElementById('cute-theme-toggle-container');
        const sunSvg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
        const moonSvg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
        
        if (!container) {
            container = parentDoc.createElement('div');
            container.id = 'cute-theme-toggle-container';
            
            const style = parentDoc.createElement('style');
            style.innerHTML = `
                #cute-theme-toggle-container {
                    position: fixed;
                    top: 70px;
                    right: 20px;
                    z-index: 9999999;
                    cursor: pointer;
                    user-select: none;
                }
                .theme-track {
                    width: 70px;
                    height: 36px;
                    border-radius: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 8px;
                    position: relative;
                    transition: all 0.3s ease;
                    box-sizing: border-box;
                }
                .theme-track.light {
                    background-color: #ffffff;
                    box-shadow: 2px 4px 0px rgba(0,0,0,0.1);
                    border: 1px solid #e0e0e0;
                }
                .theme-track.dark {
                    background-color: #2c2c2c;
                    box-shadow: 2px 4px 0px rgba(0,0,0,0.8);
                    border: 1px solid #1a1a1a;
                }
                .theme-thumb {
                    width: 28px;
                    height: 28px;
                    background-color: #FFD700;
                    border-radius: 50%;
                    position: absolute;
                    top: 4px;
                    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                .theme-track.light .theme-thumb {
                    left: 4px;
                }
                .theme-track.dark .theme-thumb {
                    left: 38px;
                }
                .icon {
                    width: 16px;
                    height: 16px;
                    z-index: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: opacity 0.3s ease, color 0.3s ease;
                }
                .theme-track.light .icon { color: #ffd700; }
                .theme-track.light .theme-thumb { background-color: #ffd1dc; color: #ffd700; }
                .theme-track.dark .icon { color: #ffffff; }
                .theme-track.dark .theme-thumb { background-color: #0033ff; color: #ffffff; }
                
                .theme-track.light .sun-icon { opacity: 0; }
                .theme-track.dark .moon-icon { opacity: 0; }
            `;
            parentDoc.head.appendChild(style);
            
            const track = parentDoc.createElement('div');
            track.className = 'theme-track';
            
            const sunContainer = parentDoc.createElement('div');
            sunContainer.className = 'icon sun-icon';
            sunContainer.innerHTML = sunSvg;
            
            const moonContainer = parentDoc.createElement('div');
            moonContainer.className = 'icon moon-icon';
            moonContainer.innerHTML = moonSvg;
            
            const thumb = parentDoc.createElement('div');
            thumb.className = 'theme-thumb';
            
            track.appendChild(sunContainer);
            track.appendChild(moonContainer);
            track.appendChild(thumb);
            container.appendChild(track);
            
            parentDoc.body.appendChild(container);
        }
        
        const currentTrack = container.querySelector('.theme-track');
        const currentThumb = container.querySelector('.theme-thumb');
        
        function updateVisuals(theme) {
            if (theme === 'light') {
                currentTrack.className = 'theme-track light';
                currentThumb.innerHTML = sunSvg;
            } else {
                currentTrack.className = 'theme-track dark';
                currentThumb.innerHTML = moonSvg;
            }
        }
        
        let currentTheme = localStorage.getItem('coachAiTheme') || 'light';
        parentDoc.documentElement.setAttribute('data-custom-theme', currentTheme);
        updateVisuals(currentTheme);
        
        // Re-attach onclick handler unconditionally so it survives Streamlit iframe unmounting
        container.onclick = function() {
            currentTheme = currentTheme === 'light' ? 'dark' : 'light';
            parentDoc.documentElement.setAttribute('data-custom-theme', currentTheme);
            localStorage.setItem('coachAiTheme', currentTheme);
            updateVisuals(currentTheme);
            
            currentTrack.style.transform = 'scale(0.95)';
            setTimeout(() => currentTrack.style.transform = 'scale(1)', 150);
        };
    </script>
    """ + load_local_js("animations.js"), height=0, width=0)
