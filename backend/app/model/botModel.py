from dataclasses import dataclass

from app.control.bot.baseBot import BaseBot
from .baseModel import BaseModel


@dataclass
class BotModel(BaseModel):
    api_key: str = None
    bot: BaseBot = None
