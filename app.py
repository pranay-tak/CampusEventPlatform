import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image

# Import local modules
from src.database import init_db, load_sample_data, get_db_connection
from src.ocr import extract_text_from_image
from src.llm import extract_structured_event_data, generate_image_prompt
from src.image_gen import generate_image_a1111
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

st.set_page_config(page_title="Campus Events", layout="wide", initial_sidebar_state="expanded")

from src.ui_styles import inject_custom_css, get_category_class
inject_custom_css()

# --- Top/Sidebar Navigation ---
with st.sidebar:
    st.title("🎓 Campus")
    st.markdown("---")
    page = st.radio("Navigation", ["Home", "Discover", "For You", "Organizer Portal"], label_visibility="collapsed")
    
    st.markdown("---")
    st.caption("Developer Panel")
    role = st.selectbox("Role", ["Student", "Organizer"])
    st.session_state.current_user_id = 1 if "Student" in role else 3

# Map new nav names to logic
if page == "Home":
    # --- Hero Section ---
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Discover Your Campus</div>
            <div class="hero-subtitle">The easiest way to find, join, and host events at CHRIST University.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Interactive Filter Bar ---
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        quick_search = st.text_input("Search events...", placeholder="Try: 'dance events today' or 'AI workshops'", label_visibility="collapsed")
    with col2:
        filter_cat = st.selectbox("Category", ["All", "Tech", "Cultural", "Sports", "Workshop", "Hackathon"], label_visibility="collapsed")
    with col3:
        filter_time = st.selectbox("Time", ["Anytime", "Today", "This Week", "This Weekend"], label_visibility="collapsed")
    
    st.write("")
    
    # --- Fetch & Render Events ---
    conn = get_db_connection()
    
    query = "SELECT MIN(id) as id, title, date, start_time, venue, description, category, generated_poster_path FROM events WHERE 1=1"
    params = []
    
    if quick_search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{quick_search}%", f"%{quick_search}%"])
    
    if filter_cat != "All":
        query += " AND category LIKE ?"
        params.append(f"%{filter_cat}%")
        
    query += " GROUP BY title, date ORDER BY date ASC LIMIT 9"
    events = conn.execute(query, params).fetchall()
    conn.close()
    
    st.markdown("### Upcoming Events")
    
    if not events:
        st.markdown("""
        <div class="empty-state">
            <h1>🏜️</h1>
            <h3>No events found</h3>
            <p>Check back later or switch up your filters!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for idx, event in enumerate(events):
            with cols[idx % 3]:
                # Streamlit container serves as the physical card (styled in CSS)
                with st.container():
                    # Poster Image
                    if event['generated_poster_path'] and os.path.exists(event['generated_poster_path']):
                        st.image(event['generated_poster_path'], use_container_width=True)
                    else:
                        # Fallback for old events lacking an image
                        st.image("https://via.placeholder.com/800x400/1e293b/ffffff?text=Event", use_container_width=True)
                    
                    # Category Badge HTML
                    cat_class = get_category_class(event['category'])
                    st.markdown(f'<span class="badge {cat_class}">{event["category"]}</span>', unsafe_allow_html=True)
                    
                    # Details
                    st.markdown(f"**{event['title']}**")
                    st.caption(f"🗓️ {event['date']} • ⏰ {event['start_time']}")
                    st.caption(f"📍 {event['venue']}")
                    
                    if st.button("Register / Details", key=f"det_{event['id']}", use_container_width=True):
                        st.info(event['description'])
                        st.markdown(f"[🔗 Open Registration Form (Google Forms)](https://forms.gle/dummy) *(Demo Link)*")
                        
                        # Generate and provide PDF
                        from src.export_pdf import generate_event_pdf
                        pdf_path = generate_event_pdf(dict(event), f"outputs/event_{event['id']}.pdf")
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📄 Download as PDF",
                                data=f,
                                file_name=f"Event_{event['title'].replace(' ', '_')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    
                    # Delete Feature (Phase 5)
                    if st.session_state.current_user_id == 3: # Organizer role
                        delete_key = f"del_{event['id']}"
                        if st.button("🗑️ Delete Event", key=delete_key, use_container_width=True):
                            st.session_state[f"confirm_delete_{event['id']}"] = True
                            st.rerun()
                            
                        if st.session_state.get(f"confirm_delete_{event['id']}", False):
                            st.warning(f"Delete '{event['title']}'? This can't be undone.")
                            col_y, col_n = st.columns(2)
                            if col_y.button("Yes, Delete", key=f"yes_{event['id']}", type="primary"):
                                conn = get_db_connection()
                                conn.execute("DELETE FROM events WHERE id = ?", (event['id'],))
                                conn.commit()
                                conn.close()
                                st.toast("Event deleted successfully!", icon="🗑️")
                                st.session_state[f"confirm_delete_{event['id']}"] = False
                                st.rerun()
                            if col_n.button("Cancel", key=f"no_{event['id']}"):
                                st.session_state[f"confirm_delete_{event['id']}"] = False
                                st.rerun()

elif page == "Discover":
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

elif page == "For You":
    st.title("Recommended for You 🎯")
    
    st.markdown("### Set Your Interests")
    interests = st.multiselect(
        "What kind of events do you love?", 
        ["Tech", "AI", "Cultural", "Sports", "Dance", "Workshop", "Hackathon", "Data Analytics"],
        default=["Tech"]
    )
    
    st.markdown("### Your Custom Feed")
    
    conn = get_db_connection()
    if interests:
        placeholders = " OR ".join(["category LIKE ?" for _ in interests] + ["title LIKE ?" for _ in interests])
        params = [f"%{i}%" for i in interests] * 2
        query = f"SELECT MIN(id) as id, title, date, start_time, venue, description, category, generated_poster_path FROM events WHERE {placeholders} GROUP BY title, date"
        recs = conn.execute(query, params).fetchall()
    else:
        recs = []
    conn.close()
    
    if not recs:
        st.info("No recommendations yet. Pick some interests above!")
    else:
        cols = st.columns(3)
        for idx, event in enumerate(recs):
            with cols[idx % 3]:
                with st.container():
                    cat_class = get_category_class(event['category'])
                    st.markdown(f'<span class="badge {cat_class}">{event["category"]}</span>', unsafe_allow_html=True)
                    st.markdown(f"**{event['title']}**")
                    st.caption(f"🗓️ {event['date']} • ⏰ {event['start_time']}")
                    st.caption(f"✨ Because you like {', '.join(interests[:2])}")
                    if st.button("Details", key=f"rec_{event['id']}", use_container_width=True):
                        st.info(event['description'])

elif page == "Organizer Portal":
    st.title("AI Event Creator 🚀")
    st.write("Upload an old poster or enter details to let AI generate your promotional content and new poster.")
    
    from src.llm import generate_social_captions
    
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 1
        st.session_state.extracted_data = {}
        st.session_state.temp_poster_path = None
        st.session_state.captions = {}
        
    if st.session_state.workflow_step == 1:
        st.subheader("Step 1: Upload Poster")
        uploaded_file = st.file_uploader("Upload Event Poster (Optional for OCR)", type=['png', 'jpg', 'jpeg'])
        
        col_up, col_skip = st.columns(2)
        with col_up:
            if st.button("Extract Details", use_container_width=True):
                if uploaded_file is not None:
                    os.makedirs("outputs", exist_ok=True)
                    temp_path = f"outputs/temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.session_state.temp_poster_path = temp_path
                    
                    with st.spinner("Extracting with OCR and LLM..."):
                        raw_text = extract_text_from_image(temp_path)
                        st.session_state.extracted_data = extract_structured_event_data(raw_text)
                    st.session_state.workflow_step = 2
                    st.rerun()
                else:
                    st.warning("Please upload a poster or click 'Create Manually'.")
        with col_skip:
            if st.button("Skip & Create Manually", use_container_width=True):
                st.session_state.extracted_data = {}
                st.session_state.workflow_step = 2
                st.rerun()
                
    elif st.session_state.workflow_step == 2:
        st.subheader("Step 2: Review & Edit Details")
        data = st.session_state.extracted_data
        
        # Fallback for missing time
        initial_time = data.get('time', '')
        if not initial_time or str(initial_time).lower() == 'none':
            initial_time = ''
            st.warning("Time was not clearly detected. Please enter it manually.")
            
        with st.form("edit_event_form"):
            new_title = st.text_input("Title", value=data.get('title', ''))
            new_date = st.text_input("Date", value=data.get('date', ''))
            new_time = st.text_input("Time", value=initial_time)
            new_venue = st.text_input("Venue", value=data.get('venue', ''))
            new_category = st.text_input("Category", value=data.get('category', ''))
            new_description = st.text_area("Description", value=data.get('description', ''))
            
            poster_option = "Generate new AI poster"
            if st.session_state.temp_poster_path:
                poster_option = st.radio("Poster Image", ["Use original uploaded poster", "Generate new AI poster"])
                
            st.markdown("**Promotional Content**")
            gen_ig = st.checkbox("Generate Instagram Caption", value=True)
            gen_li = st.checkbox("Generate LinkedIn Caption", value=True)
            
            if st.form_submit_button("Generate & Publish"):
                if not new_title.strip():
                    st.error("⚠️ Please enter at least a Title for the event before proceeding!")
                else:
                    st.session_state.poster_option = poster_option if st.session_state.temp_poster_path else "Generate new AI poster"
                    st.session_state.gen_ig = gen_ig
                    st.session_state.gen_li = gen_li
                    st.session_state.extracted_data = {
                        'title': new_title,
                        'date': new_date,
                    'time': new_time,
                    'venue': new_venue,
                    'category': new_category,
                    'description': new_description
                }
                st.session_state.workflow_step = 3
                st.rerun()
                
    elif st.session_state.workflow_step == 3:
        st.subheader("Step 3: Final Output")
        
        if not st.session_state.captions:
            with st.spinner("Processing final assets..."):
                from src.image_gen import generate_image_a1111
                st.session_state.captions = generate_social_captions(st.session_state.extracted_data)
                
                import time
                import shutil
                timestamp = int(time.time())
                
                if st.session_state.get('poster_option') == "Use original uploaded poster" and st.session_state.temp_poster_path:
                    final_poster_path = f"outputs/final_event_{timestamp}.png"
                    shutil.copy(st.session_state.temp_poster_path, final_poster_path)
                    st.session_state.final_poster_path = final_poster_path
                else:
                    image_prompt = generate_image_prompt(st.session_state.extracted_data)
                    base_img = generate_image_a1111(image_prompt)
                    final_poster_path = overlay_event_text(base_img, st.session_state.extracted_data, f"outputs/final_event_{timestamp}.png")
                    st.session_state.final_poster_path = final_poster_path
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.final_poster_path, caption="Final Event Poster")
            
        with col2:
            st.subheader("Social Captions")
            
            if st.session_state.get('gen_ig', True):
                ig_caption = st.text_area("Instagram Caption", value=st.session_state.captions.get('instagram', ''), height=150)
                st.code(ig_caption, language="text") # Easy copy button
                
            if st.session_state.get('gen_li', True):
                li_caption = st.text_area("LinkedIn Caption", value=st.session_state.captions.get('linkedin', ''), height=150)
                st.code(li_caption, language="text") # Easy copy button
            
            if not st.session_state.get('gen_ig', True) and not st.session_state.get('gen_li', True):
                st.info("You chose to skip generating social media captions.")
            
            if st.button("Publish Event"):
                conn = get_db_connection()
                conn.execute("""
                    INSERT INTO events (title, description, category, date, start_time, venue, generated_poster_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (st.session_state.extracted_data.get('title'), 
                      st.session_state.extracted_data.get('description'), 
                      st.session_state.extracted_data.get('category'), 
                      st.session_state.extracted_data.get('date'), 
                      st.session_state.extracted_data.get('time'), 
                      st.session_state.extracted_data.get('venue'), 
                      st.session_state.final_poster_path))
                conn.commit()
                conn.close()
                st.success("Event Published to Database!")
                st.session_state.workflow_step = 1 # Reset

