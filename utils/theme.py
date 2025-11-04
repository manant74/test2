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
    
    /* Main app background with deep space black and starfield */
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.02) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.01) 0%, transparent 50%),
            linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
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
    </style>
    """, unsafe_allow_html=True)
