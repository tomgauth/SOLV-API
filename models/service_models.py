from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, List
from .base_models import BaseRequest, BaseResponse

# Supported languages and their codes
SUPPORTED_LANGUAGES = {
    "English (US)": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "German": "de-DE",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN"
}

class TextToSpeechRequest(BaseRequest):
    """Request model for text-to-speech conversion."""
    text: str = Field(..., description="The text to convert to speech")
    language_code: str = Field(..., description="Language code (e.g., 'en-US', 'fr-FR')")
    gender: Literal['male', 'female'] = Field(default='female', description="Voice gender")
    provider: Literal['elevenlabs', 'google'] = Field(default='elevenlabs', description="TTS provider to use")
    voice_id: Optional[str] = Field(None, description="Specific voice ID (for ElevenLabs)")
    model: Optional[str] = Field(default="eleven_multilingual_v2", description="Model to use for generation")

class TextToSpeechResponse(BaseResponse):
    """Response model for text-to-speech conversion."""
    audio_content: bytes = Field(..., description="Binary audio data")
    audio_format: str = Field(..., description="Audio format (e.g., 'mp3', 'wav')")
    voice_id: Optional[str] = Field(None, description="ID of the voice used")
    duration_ms: Optional[int] = Field(None, description="Duration of the audio in milliseconds")
    provider: str = Field(..., description="Provider used for generation")
    language_code: str = Field(..., description="Language code used")
    gender: str = Field(..., description="Gender of the voice used") 