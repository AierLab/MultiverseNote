from dataclasses import dataclass

from app.control.bot.baseBot import BaseBot


@dataclass
class BotModel:
    api_key: str = None
    bot: BaseBot = None
