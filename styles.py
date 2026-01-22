def get_global_styles():
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@400;600;700&display=swap');
    
    :root {
        --bg-color: #050505;
        --card-bg: rgba(25, 25, 25, 0.6);
        --accent: #8b5cf6;
        --text-primary: #e5e5e5;
        --text-secondary: #a3a3a3;
        --border-color: rgba(255, 255, 255, 0.1);
        --font-heading: 'Outfit', sans-serif;
        --font-body: 'Inter', sans-serif;
    }
    
    html, body, [class*="css"] {
        font-family: var(--font-body);
        color: var(--text-primary);
        background-color: var(--bg-color);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        font-weight: 600;
        color: #fff;
    }

    /* Glassmorphism Card Utils */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.1);
        border-color: rgba(139, 92, 246, 0.3);
    }

    /* Video Container specific adjustments */
    .video-wrapper {
        position: relative; 
        border-radius: 16px; 
        overflow: hidden; 
        background: #000;
        border: 1px solid #333;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    
    /* Stats Circular Progress (Mock CSS for visuals) */
    .stat-circle {
        position: relative;
        width: 80px; 
        height: 80px;
        border-radius: 50%;
        background: conic-gradient(var(--accent) 0% 80%, #333 80% 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stat-inner {
        width: 65px; 
        height: 65px; 
        background: #1e1e1e; 
        border-radius: 50%;
        display: flex; 
        flex-direction: column;
        align-items: center; 
        justify-content: center;
    }
    .stat-value { font-weight: bold; font-size: 1.1rem; color: #fff; }
    .stat-label { font-size: 0.6rem; color: #888; text-transform: uppercase; }

    /* Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2a2a2a, #1a1a1a);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: var(--accent);
        border-color: var(--accent);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Control Bar Container */
    .control-bar-container {
        display: flex;
        align-items: center;
        justify-content: space-around;
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid var(--border-color);
        padding: 2rem;
        border-radius: 20px;
    }

</style>
"""
