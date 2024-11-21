# THis test file ensures the general functionality of the application by testing the API endpoints.

import os
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest

from app.dao.configDataManager import ConfigManager
from app.view.appView import AppView

@pytest.fixture
def client():
    # Get the absolute path to the config file
    config_path = 'storage/config/main_config.yaml'
    # config_path = '../../storage/config/main_config.yaml'
    config_manager = ConfigManager(config_path)
    flask_app = AppView(config_manager).app
    with flask_app.test_client() as client:
        yield client


def test_sanity_check(client):
    assert True


# It takes me forever to generate an OpenAI API key for no apparent reason
# Should work fine currently not passing without setting the key in main_config.yaml
def test_ask_post(client):
    response = client.post('/ask', json={'content': 'test', "agent_name": "girl_jk"})
    assert response.status_code == 200
    assert type(response.json['response']) == str and len(response.json['response']) > 0


def test_session_get(client):
    response = client.get('/session')
    assert response.status_code == 200
    assert response.json['id'] is not None


def test_session_put(client):
    response = client.put('/session', json={'content': 'test', 'role_name': 'user'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_session_put_failure(client):
    response = client.put('/session', json={'content': 'test'})
    assert response.status_code == 400
    assert response.json['status'] == 'failure'


def test_session_delete(client):
    curr_session_id = client.get('/session').json['id']
    response = client.delete('/session', json={'message_id': curr_session_id})
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_session_delete_failure(client):
    response = client.delete('/session', json={})
    assert response.status_code == 400
    assert response.json['status'] == 'failure'


def test_history_get(client):
    response = client.get('/history')
    assert response.status_code == 200
    assert isinstance(response.json, list) and len(response.json) > 0


def test_history_put(client):
    response = client.put('/history')
    curr_session_id = response.json
    session_list = client.get('/history').json
    assert response.status_code == 200
    assert curr_session_id in session_list


def test_history_delete(client):
    session_list = client.get('/history').json
    response = client.delete('/history', json={'session_id': session_list[0]})
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_history_delete_failure(client):
    response = client.delete('/history', json={})
    assert response.status_code == 400
    assert response.json['status'] == 'failure'


def test_config_get(client):
    curr_session_id = client.get('/session').json['id']
    response = client.get(f'/config/{curr_session_id}')
    assert response.status_code == 200
    assert response.json[curr_session_id] is not None


def test_config_get_failure(client):
    response = client.get('/config/test')
    assert response.status_code == 200
    assert 'Attribute test not found in ConfigModel' in response.json['test']


def test_config_post(client):
    curr_session_id = client.get('/session').json['id']
    response = client.post(f'/config/{curr_session_id}', json={'value': 'test'})
    assert response.status_code == 200
    assert response.json['status'] == 'updated'


def test_bots_get(client):
    response = client.get('/bots')
    assert response.status_code == 200
    assert isinstance(response.json, list) and len(response.json) > 0
