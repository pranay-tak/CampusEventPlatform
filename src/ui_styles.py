import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Global Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Default Header and Footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    footer {visibility: hidden;}
    
    /* Animated Hero Background */
    .hero-container {
        background: linear-gradient(135deg, #d946ef, #7e22ce, #1e1b4b, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        background: -webkit-linear-gradient(45deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
    }

    /* Event Card Hover Effects */
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 15px;
        background-color: #1e293b;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* Category Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .badge-tech { background: rgba(20, 184, 166, 0.2); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.3); }
    .badge-cultural { background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(244,114,182,0.3); }
    .badge-sports { background: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
    .badge-workshop { background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(129,140,248,0.3); }
    .badge-hackathon { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-default { background: rgba(148, 163, 184, 0.2); color: #cbd5e1; border: 1px solid rgba(203,213,225,0.3); }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: #0f172a;
        border-radius: 20px;
        border: 1px dashed #334155;
        color: #64748b;
    }
    .empty-state h3 { color: #94a3b8; }
    
    </style>
    """, unsafe_allow_html=True)

def get_category_class(category):
    cat = str(category).lower()
    if 'tech' in cat or 'ai' in cat or 'data' in cat or 'coding' in cat:
        return 'badge-tech'
    elif 'cult' in cat or 'dance' in cat or 'music' in cat:
        return 'badge-cultural'
    elif 'sport' in cat or 'basket' in cat:
        return 'badge-sports'
    elif 'work' in cat or 'semi' in cat:
        return 'badge-workshop'
    elif 'hack' in cat or 'comp' in cat:
        return 'badge-hackathon'
    else:
        return 'badge-default'
