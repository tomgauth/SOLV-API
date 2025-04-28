from typing import Dict, Type
from .base_service import BaseService
from .text_to_speech_service import TextToSpeechService

class ServiceRegistry:
    """Registry for all services in the application."""
    
    _services: Dict[str, BaseService] = {}
    
    @classmethod
    def register(cls, name: str, service: BaseService):
        """Register a new service."""
        cls._services[name] = service
    
    @classmethod
    def get(cls, name: str) -> BaseService:
        """Get a service by name."""
        if name not in cls._services:
            raise ValueError(f"Service '{name}' not found in registry")
        return cls._services[name]
    
    @classmethod
    def list_services(cls) -> Dict[str, Type[BaseService]]:
        """List all registered services."""
        return cls._services.copy()

# Register the Text-to-Speech service
ServiceRegistry.register('text_to_speech', TextToSpeechService()) 