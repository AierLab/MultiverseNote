from .openaiBot import OpenAIBot
from .petalsBot import PetalsBot
from .wenxinBot import WenxinBot

# Optional: Initialize or configure models here if necessary
# For example, you could load bot configurations or API keys from environment variables

# Export the models for easy import elsewhere in your application
__all__ = ['OpenAIBot', 'PetalsBot', 'WenxinBot']
