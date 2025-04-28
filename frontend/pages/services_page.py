import streamlit as st
from services.service_registry import ServiceRegistry

def show_services_page():
    """
    Display the services status page showing all available services and their configuration status.
    """
    st.title("Services Status")
    
    # Get all registered services from the registry
    # The registry is a singleton that maintains a list of all available services
    services = ServiceRegistry.list_services()
    
    if not services:
        st.info("No services are currently registered.")
        return
    
    # Display each service in an expandable section
    for service_name, service in services.items():
        with st.expander(f"Service: {service_name}"):
            # Show basic service information
            st.write("Status: Active")
            st.write(f"Type: {type(service).__name__}")
            
            # For Text-to-Speech service, show additional configuration details
            if service_name == 'text_to_speech':
                # Check ElevenLabs API configuration
                if hasattr(service, 'elevenlabs_api_key') and service.elevenlabs_api_key:
                    st.success("✅ ElevenLabs API configured")
                else:
                    st.error("❌ ElevenLabs API key not configured")
                
                # Check Google Cloud TTS configuration
                if hasattr(service, 'google_client') and service.google_client:
                    st.success("✅ Google Cloud TTS configured")
                else:
                    st.error("❌ Google Cloud TTS not configured")
                
                # Display supported languages
                st.markdown("#### Supported Languages")
                st.markdown("""
                - English (US)
                - French
                - Spanish
                - German
                - Italian
                - Portuguese
                - Japanese
                - Korean
                - Chinese
                """)

if __name__ == "__main__":
    show_services_page() 