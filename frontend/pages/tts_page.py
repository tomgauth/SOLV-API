import streamlit as st
import base64
from io import BytesIO
from models.service_models import TextToSpeechRequest, SUPPORTED_LANGUAGES
from services.service_registry import ServiceRegistry

def show_tts_page():
    st.title("Text to Speech")
    
    with st.form("tts_form"):
        # Text input
        text = st.text_area("Enter text to convert to speech", height=150)
        
        # Language selection
        language_name = st.selectbox(
            "Select Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=0
        )
        
        # Voice options
        col1, col2 = st.columns(2)
        with col1:
            provider = st.selectbox(
                "Select Provider",
                options=["ElevenLabs", "Google"],
                index=0
            )
        with col2:
            gender = st.selectbox(
                "Select Voice Gender",
                options=["MALE", "FEMALE"],
                index=0
            )
        
        # Submit button
        submitted = st.form_submit_button("Generate Speech")
        
        if submitted and text:
            try:
                # Create request
                request = TextToSpeechRequest(
                    text=text,
                    language_code=SUPPORTED_LANGUAGES[language_name],
                    provider=provider.upper(),
                    gender=gender
                )
                
                # Get TTS service
                tts_service = ServiceRegistry.get_instance().get_service('text_to_speech')
                
                # Generate speech
                response = tts_service.process(request)
                
                # Create audio player
                audio_b64 = base64.b64encode(response.audio_content).decode()
                audio_tag = f'<audio controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
                st.markdown(audio_tag, unsafe_allow_html=True)
                
                # Display additional info
                st.info(f"""
                    Duration: {response.duration_ms/1000:.2f} seconds
                    Voice ID: {response.voice_id}
                    Format: {response.audio_format}
                """)
                
            except Exception as e:
                st.error(f"Error generating speech: {str(e)}")
        elif submitted:
            st.warning("Please enter some text to convert to speech.")

    # Add some helpful information
    with st.expander("About Text-to-Speech Service"):
        st.write("""
        This service converts text to natural-sounding speech using two providers:
        
        - **ElevenLabs**: High-quality, expressive voices
        - **Google Cloud TTS**: Professional, clear voices
        
        Choose the provider and voice options that best suit your needs.
        """)

if __name__ == "__main__":
    show_tts_page() 