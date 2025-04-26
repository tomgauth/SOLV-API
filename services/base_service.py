from abc import ABC, abstractmethod
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """Base class for all services in the application."""
    
    @abstractmethod
    def process(self, input_data: BaseModel) -> BaseModel:
        """
        Process the input data and return the result.
        
        Args:
            input_data: A Pydantic model containing the input data
            
        Returns:
            A Pydantic model containing the processed result
        """
        pass
    
    def _log_input(self, input_data: BaseModel):
        """Log the input data for debugging purposes."""
        logger.info(f"Processing input for {self.__class__.__name__}: {input_data}")
    
    def _log_output(self, output_data: BaseModel):
        """Log the output data for debugging purposes."""
        logger.info(f"Output from {self.__class__.__name__}: {output_data}") 