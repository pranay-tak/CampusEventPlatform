import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image

# Import local modules
from src.database import init_db, load_sample_data, get_db_connection
from src.ocr import extract_text_from_image
from src.llm import extract_structured_event_data, generate_promotional_content, generate_image_prompt
from src.image_gen import generate_image_comfyui
from src.utils import overlay_event_text
from src.search import process_natural_language_search
from src.recommendations import get_recommendations

# --- Initialization ---
if 'db_initialized' not in st.session_state:
    init_db()
    load_sample_data()
    st.session_state.db_initialized = True

if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = 1 # Default to Pranay (Student)

st.set_page_config(page_title="AI Campus Events", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Student Dashboard", "Discover Events", "My Recommendations", "Organizer Portal"])

# Simulated User Switcher
st.sidebar.markdown("---")
st.sidebar.subheader("Dev Tools")
role = st.sidebar.selectbox("Simulate User", ["Student (Pranay)", "Organizer (Tech Club)"])
if "Student" in role:
    st.session_state.current_user_id = 1
else:
    st.session_state.current_user_id = 3

# --- Pages ---

if page == "Student Dashboard":
    st.title("Welcome to Campus Events 🎓")
    st.write("Never miss an event on campus again.")
    
    conn = get_db_connection()
    events = conn.execute("SELECT * FROM events ORDER BY date ASC LIMIT 3").fetchall()
    conn.close()
    
    st.subheader("Upcoming Events")
    cols = st.columns(3)
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            st.card_container = st.container(border=True)
            if event['generated_poster_path'] and os.path.exists(event['generated_poster_path']):
                st.image(event['generated_poster_path'], use_column_width=True)
            st.subheader(event['title'])
            st.write(f"📅 {event['date']} | ⏰ {event['start_time']}")
            st.write(f"📍 {event['venue']}")
            if st.button("Details", key=f"det_{event['id']}"):
                st.info(event['description'])

elif page == "Discover Events":
    st.title("Discover Events 🔍")
    
    search_query = st.text_input("Ask AI: e.g., 'Show me AI hackathons this weekend'")
    if search_query:
        with st.spinner("AI is interpreting your request..."):
            results = process_natural_language_search(search_query)
        
        if results:
            st.success(f"Found {len(results)} events matching your query.")
            for event in results:
                with st.expander(f"{event['title']} - {event['date']}"):
                    st.write(f"**Category:** {event['category']}")
                    st.write(f"**Venue:** {event['venue']}")
                    st.write(event['description'])
        else:
            st.warning("No events found matching those criteria.")

elif page == "My Recommendations":
    st.title("Recommended for You 🎯")
    
    recs = get_recommendations(st.session_state.current_user_id)
    if not recs:
        st.info("No recommendations yet. Interact with more events!")
    else:
        for rec in recs:
            event = rec['event']
            st.markdown(f"### {event['title']}")
            st.caption(f"✨ {rec['reason']}")
            st.write(f"📅 {event['date']} at {event['venue']}")
            st.divider()

elif page == "Organizer Portal":
    st.title("AI Event Creator 🚀")
    st.write("Upload an old poster or enter details to let AI generate your promotional content and new poster.")
    
    uploaded_file = st.file_uploader("Upload Event Poster (Optional for OCR)", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Start AI Workflow"):
        if uploaded_file is not None:
            # 1. OCR
            st.info("1. Running Local OCR...")
            os.makedirs("outputs", exist_ok=True)
            temp_path = f"outputs/temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            raw_text = extract_text_from_image(temp_path)
            st.write("Extracted Text:", raw_text)
            
            # 2. Local LLM Structuring
            st.info("2. Structuring data with Local LLM (Ollama)...")
            structured_data = extract_structured_event_data(raw_text)
            st.json(structured_data)
            
            # 3. LLM Content Gen
            st.info("3. Generating Promotional Content...")
            promo_content = generate_promotional_content(structured_data)
            st.write(promo_content)
            
            # 4. Image Generation
            st.info("4. Generating Image Prompt & Local Poster...")
            image_prompt = generate_image_prompt(structured_data)
            st.write(f"**Image Prompt:** {image_prompt}")
            
            base_image_path = generate_image_comfyui(image_prompt)
            
            # 5. Overlay Text
            final_poster_path = overlay_event_text(base_image_path, structured_data, f"outputs/final_{uploaded_file.name}")
            
            st.success("Workflow Complete!")
            st.image(final_poster_path, caption="Final AI Generated Poster")
            
            # Save to DB (mock logic for saving)
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO events (title, description, category, date, venue, generated_poster_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (structured_data.get('title', 'AI Event'), 
                  structured_data.get('description', ''), 
                  structured_data.get('category', 'Other'), 
                  structured_data.get('date', ''), 
                  structured_data.get('venue', ''), 
                  final_poster_path))
            conn.commit()
            conn.close()
            st.success("Event Published to Database!")
        else:
            st.warning("Please upload a poster to test the full OCR -> LLM -> Image workflow.")
