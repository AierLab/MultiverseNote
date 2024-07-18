# app/model/__init__.py

from .openaiModel import OpenAIModel
from .petalsModel import PetalsModel
from .wenxinModel import WenxinModel

# Optional: Initialize or configure models here if necessary
# For example, you could load model configurations or API keys from environment variables

# Export the models for easy import elsewhere in your application
__all__ = ['OpenAIModel', 'PetalsModel', 'WenxinModel']
