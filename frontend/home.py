import streamlit as st

def show_home_page():
    st.title("Welcome to SOLV API Services")
    
    st.markdown("""
    This application provides access to various AI and automation services.
    Choose a service from the sidebar to get started.
    
    ### Available Services:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("#### Text-to-Speech\nConvert text to natural-sounding speech using multiple providers.")
        if st.button("Try Text-to-Speech"):
            st.session_state.page = "Text-to-Speech"
            st.rerun()
    
    with col2:
        st.info("#### Services Status\nCheck the status of all available services.")
        if st.button("View Services"):
            st.session_state.page = "Services"
            st.rerun()

if __name__ == "__main__":
    show_home_page() 