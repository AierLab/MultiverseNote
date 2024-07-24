# Abstract class

from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def ask_model(self, input_text, context=None):
        """
        Method to be implemented by all derived classes to process input and return model output.
        """
        pass
