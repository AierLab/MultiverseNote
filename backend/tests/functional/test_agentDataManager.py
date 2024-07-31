from app.dao.agentDataManager import AgentManager
from app.model.agentModel import AgentModel


def test_load():
    agent_manager = AgentManager(r"../storage/agent")
    agent = agent_manager.load("base")
    print(agent)
    agent.prompt = ""
    agent_reference = AgentModel(name='base', args=['query'], prompt="")
    assert agent_reference == agent
