import streamlit as st
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.internal_api import call_service
from models.base_models import BaseRequest, BaseResponse

def main():
    st.title("SOLV API Dashboard")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Services"])
    
    if page == "Home":
        show_home_page()
    elif page == "Services":
        show_services_page()

def show_home_page():
    st.header("Welcome to SOLV API")
    st.write("""
    This is the main dashboard for the SOLV API application.
    Use the sidebar to navigate between different sections.
    """)
    
    # Example of how to call a service
    if st.button("Test Service"):
        result = call_service("example_service", BaseRequest())
        st.write("Service Response:", result)

def show_services_page():
    st.header("Available Services")
    st.write("""
    This page shows all available services and their status.
    """)
    
    # TODO: Add service status monitoring
    st.info("Service status monitoring coming soon!")

if __name__ == "__main__":
    main() 