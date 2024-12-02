# Manages interactions with the Petals framework, enabling decentralized bot operations as described earlier.
from .baseBot import BaseBot
from app.model.dataModel import MessageModel, SessionModel
from app.model.agentModel import AgentModel

class PetalsBot(BaseBot):
    def ask(self,
            message: MessageModel,
            agent: AgentModel,
            session: SessionModel) -> MessageModel:        # Interaction with Petals decentralized network
        raise NotImplementedError
