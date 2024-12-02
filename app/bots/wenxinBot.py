# Interfaces with the Wenxin API (likely another AI or ML service), handling specific functionalities provided by this service.
from .baseBot import BaseBot
from app.model.dataModel import MessageModel, SessionModel
from app.model.agentModel import AgentModel

class WenxinBot(BaseBot):
    def ask(self,
            message: MessageModel,
            agent: AgentModel,
            session: SessionModel) -> MessageModel:        # Call to Wenxin API
        raise NotImplementedError
