import os
import logging
from typing import Optional, Dict, List
from elevenlabs import generate, set_api_key, voices, Voice
from google.cloud import texttospeech
from .base_service import BaseService
from models.service_models import TextToSpeechRequest, TextToSpeechResponse, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

class TextToSpeechService(BaseService):
    """Service for converting text to speech using various providers."""
    
    def __init__(self):
        """Initialize the service with API keys."""
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        if self.elevenlabs_api_key:
            set_api_key(self.elevenlabs_api_key)
        
        # Initialize Google Cloud client if credentials are available
        self.google_client = None
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                self.google_client = texttospeech.TextToSpeechClient()
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud client: {e}")
        
        # Cache for available voices
        self._available_voices: Dict[str, List[Voice]] = {}
    
    def _get_available_voices(self) -> Dict[str, List[Voice]]:
        """Get and cache available voices from ElevenLabs."""
        if not self._available_voices:
            try:
                voices_list = voices()
                # Group voices by language
                for voice in voices_list:
                    lang = voice.labels.get('language', 'unknown')
                    if lang not in self._available_voices:
                        self._available_voices[lang] = []
                    self._available_voices[lang].append(voice)
            except Exception as e:
                logger.error(f"Error getting ElevenLabs voices: {e}")
                return {}
        return self._available_voices
    
    def _get_elevenlabs_voice(self, language_code: str, gender: str) -> Optional[str]:
        """Get the appropriate ElevenLabs voice ID based on language and gender."""
        try:
            available_voices = self._get_available_voices()
            lang_voices = available_voices.get(language_code, [])
            
            # Filter voices by gender
            matching_voices = [
                voice for voice in lang_voices
                if voice.labels.get('gender') == gender
            ]
            
            if not matching_voices:
                logger.warning(f"No voices found for {language_code} {gender}")
                return None
                
            return matching_voices[0].voice_id
        except Exception as e:
            logger.error(f"Error getting ElevenLabs voices: {e}")
            return None
    
    def _generate_with_elevenlabs(self, request: TextToSpeechRequest) -> TextToSpeechResponse:
        """Generate speech using ElevenLabs API."""
        try:
            voice_id = request.voice_id or self._get_elevenlabs_voice(
                request.language_code, request.gender
            )
            if not voice_id:
                raise ValueError(f"No suitable voice found for {request.language_code} {request.gender}")
            
            audio = generate(
                text=request.text,
                voice=voice_id,
                model=request.model
            )
            
            return TextToSpeechResponse(
                audio_content=audio,
                audio_format="mp3",
                voice_id=voice_id,
                provider="elevenlabs",
                language_code=request.language_code,
                gender=request.gender
            )
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            raise
    
    def _generate_with_google(self, request: TextToSpeechRequest) -> TextToSpeechResponse:
        """Generate speech using Google Cloud TTS API."""
        if not self.google_client:
            raise ValueError("Google Cloud client not initialized")
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=request.text)
            
            # Map gender to SSML gender
            ssml_gender = (
                texttospeech.SsmlVoiceGender.FEMALE
                if request.gender == 'female'
                else texttospeech.SsmlVoiceGender.MALE
            )
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=request.language_code,
                ssml_gender=ssml_gender
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.google_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return TextToSpeechResponse(
                audio_content=response.audio_content,
                audio_format="mp3",
                voice_id=f"{request.language_code}-{request.gender}",
                provider="google",
                language_code=request.language_code,
                gender=request.gender
            )
        except Exception as e:
            logger.error(f"Google Cloud TTS error: {e}")
            raise
    
    def process(self, input_data: TextToSpeechRequest) -> TextToSpeechResponse:
        """
        Process the text-to-speech request.
        
        Args:
            input_data: TextToSpeechRequest containing text and parameters
            
        Returns:
            TextToSpeechResponse with audio content
        """
        self._log_input(input_data)
        
        try:
            if input_data.provider == 'elevenlabs':
                if not self.elevenlabs_api_key:
                    raise ValueError("ElevenLabs API key not configured")
                result = self._generate_with_elevenlabs(input_data)
            else:  # google
                if not self.google_client:
                    raise ValueError("Google Cloud credentials not configured")
                result = self._generate_with_google(input_data)
            
            self._log_output(result)
            return result
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            raise 