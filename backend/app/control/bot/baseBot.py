# Abstract class

from abc import ABC, abstractmethod


class BaseBot(ABC):

    def init_model(self, **kwargs):
        pass

    @abstractmethod
    def ask_model(self, input_text, context=None):
        """
        Method to be implemented by all derived classes to process input and return bot output.
        """
        pass
