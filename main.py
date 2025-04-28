import streamlit as st
import sys
from pathlib import Path

# Add the frontend directory to the Python path
frontend_dir = Path(__file__).parent / "frontend"
sys.path.append(str(frontend_dir))

from frontend.home import show_home_page
from frontend.pages.tts_page import show_tts_page
from frontend.pages.services_page import show_services_page

def main():
    st.set_page_config(
        page_title="SOLV API Services",
        page_icon="🎯",
        layout="wide"
    )
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Home", "Text-to-Speech", "Services"])
    
    if page == "Home":
        show_home_page()
    elif page == "Text-to-Speech":
        show_tts_page()
    elif page == "Services":
        show_services_page()

if __name__ == "__main__":
    main() 