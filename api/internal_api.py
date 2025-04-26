import logging
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from services.service_registry import ServiceRegistry
from models.base_models import ErrorResponse

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)

def call_service(service_name: str, input_data: T) -> R:
    """
    Call a service with the given input data.
    
    Args:
        service_name: Name of the service to call
        input_data: Input data model
        
    Returns:
        Response model from the service
        
    Raises:
        ValueError: If service not found
        Exception: If service processing fails
    """
    try:
        service = ServiceRegistry.get(service_name)
        logger.info(f"Calling service {service_name} with input: {input_data}")
        
        result = service.process(input_data)
        logger.info(f"Service {service_name} returned: {result}")
        
        return result
        
    except ValueError as e:
        logger.error(f"Service error: {str(e)}")
        return ErrorResponse(error=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in service {service_name}: {str(e)}")
        return ErrorResponse(error=f"Internal error: {str(e)}") 