"""
Star Wars Theme Engine for VibeTheForce
Provides custom CSS styling and theme constants
"""

import streamlit as st

# Rating colors mapping (1-5 stars) - Imperial theme
RATING_COLORS = {
    1: "#666666",  # Grigio scuro - Youngling
    2: "#0066CC",  # Blu - Padawan
    3: "#00FF00",  # Verde - Cavaliere Jedi
    4: "#8A2BE2",  # Viola - Maestro Jedi
    5: "#FFD700"   # Oro - Gran Maestro
}

# Rating labels with Star Wars ranks
RATING_LABELS = {
    1: "⭐ Youngling",
    2: "⭐⭐ Padawan",
    3: "⭐⭐⭐ Cavaliere Jedi",
    4: "⭐⭐⭐⭐ Maestro Jedi",
    5: "⭐⭐⭐⭐⭐ Gran Maestro"
}


def apply_star_wars_theme():
    """
    Apply Star Wars theme to Streamlit app with custom CSS
    Includes background gradient, button styling, typography, and animations
    """
    st.markdown("""
    <style>
    /* Import Star Wars inspired font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main app background with deep space black and animated starfield */
    .stApp {
        background: 
            /* Animated stars */
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ddd, transparent),
            /* More stars */
            radial-gradient(1px 1px at 200px 90px, #fff, transparent),
            radial-gradient(1px 1px at 240px 50px, rgba(255,255,255,0.7), transparent),
            radial-gradient(2px 2px at 280px 10px, #eee, transparent),
            radial-gradient(1px 1px at 320px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 360px 40px, #fff, transparent),
            /* Additional scattered stars */
            radial-gradient(1px 1px at 50px 120px, rgba(255,255,255,0.6), transparent),
            radial-gradient(1px 1px at 100px 150px, #fff, transparent),
            radial-gradient(2px 2px at 150px 100px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 250px 140px, #ddd, transparent),
            radial-gradient(1px 1px at 300px 120px, rgba(255,255,255,0.7), transparent),
            /* Base gradient */
            linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a2e 50%, #16213e 75%, #000000 100%);
        background-size: 400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px,
                         400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px,
                         400px 200px, 400px 200px, 400px 200px, 400px 200px, 400px 200px,
                         100% 100%;
        animation: starfield 120s linear infinite;
    }
    
    /* Starfield animation */
    @keyframes starfield {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0, 0 0; }
        100% { background-position: -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, -400px 0, 0 0; }
    }
    
    /* Streamlit header styling to match the theme */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1a2e 50%, #16213e 75%, #000000 100%) !important;
        border-bottom: 1px solid #333333;
        height: 60px;
    }
    
    /* Streamlit toolbar styling */
    .stToolbar {
        background: transparent !important;
    }
    
    /* Main header container */
    [data-testid="stHeader"] > div {
        background: transparent !important;
    }
    
    /* Button styling with Imperial gray/white theme */
    .stButton>button {
        background: linear-gradient(145deg, #e6e6e6 0%, #cccccc 50%, #b3b3b3 100%);
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #999999;
        font-size: 18px;
        padding: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* Button hover animation with metallic glow effect */
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #ffffff, 0 0 30px #cccccc, inset 0 1px 0 rgba(255, 255, 255, 0.5);
        background: linear-gradient(145deg, #f0f0f0 0%, #d9d9d9 50%, #c0c0c0 100%);
    }
    
    /* Button active state */
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Headers with Imperial white/silver and glow */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0 0 10px #ffffff, 0 0 20px #cccccc, 0 0 30px #999999;
        font-weight: 700;
    }
    
    /* Metric cards with Imperial panel styling */
    .stMetric {
        background: linear-gradient(145deg, rgba(51, 51, 51, 0.3) 0%, rgba(34, 34, 34, 0.3) 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #666666;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Metric label styling */
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Metric value styling */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 0 0 5px #ffffff;
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        background: linear-gradient(145deg, rgba(34, 34, 34, 0.8) 0%, rgba(17, 17, 17, 0.8) 100%);
        color: #ffffff;
        border: 1px solid #666666;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Text area focus state */
    .stTextArea>div>div>textarea:focus {
        border-color: #999999;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        border-right: 1px solid #333333;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .css-1d391kg {
        color: #ffffff;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1);
        border: 1px solid #00FF00;
        border-radius: 8px;
        color: #00FF00;
    }
    
    /* Error message styling */
    .stError {
        background-color: rgba(255, 0, 0, 0.1);
        border: 1px solid #FF0000;
        border-radius: 8px;
        color: #FF0000;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(145deg, rgba(51, 51, 51, 0.2) 0%, rgba(34, 34, 34, 0.2) 100%);
        border: 1px solid #666666;
        border-radius: 8px;
        color: #ffffff;
    }
    
    /* General text color */
    p, span, div {
        color: #FFFFFF;
    }
    
    /* Link styling */
    a {
        color: #cccccc;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #ffffff;
        text-shadow: 0 0 5px #ffffff;
    }
    
    /* Plotly chart background */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Column styling for voting buttons */
    [data-testid="column"] {
        padding: 5px;
    }
    
    /* Markdown text styling */
    .stMarkdown {
        color: #FFFFFF;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, rgba(51, 51, 51, 0.3) 0%, rgba(34, 34, 34, 0.3) 100%);
        border: 1px solid #666666;
        border-radius: 8px;
        color: #ffffff !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #ffffff !important;
    }
    
    /* Custom animation for page load */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Twinkling stars effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(1px 1px at 25px 25px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 75px 75px, rgba(255,255,255,0.6), transparent),
            radial-gradient(1px 1px at 125px 125px, rgba(255,255,255,0.9), transparent),
            radial-gradient(1px 1px at 175px 175px, rgba(255,255,255,0.7), transparent),
            radial-gradient(1px 1px at 225px 225px, rgba(255,255,255,0.8), transparent);
        background-size: 250px 250px;
        animation: twinkle 4s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.3; }
        50% { opacity: 0.8; }
        100% { opacity: 0.3; }
    }
    
    /* Additional distant stars layer */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(0.5px 0.5px at 50px 100px, rgba(255,255,255,0.4), transparent),
            radial-gradient(0.5px 0.5px at 150px 200px, rgba(255,255,255,0.3), transparent),
            radial-gradient(0.5px 0.5px at 300px 50px, rgba(255,255,255,0.5), transparent),
            radial-gradient(0.5px 0.5px at 400px 150px, rgba(255,255,255,0.3), transparent);
        background-size: 500px 300px;
        animation: slowTwinkle 8s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: -2;
    }
    
    @keyframes slowTwinkle {
        0% { opacity: 0.2; }
        100% { opacity: 0.6; }
    }
    </style>
    """, unsafe_allow_html=True)
