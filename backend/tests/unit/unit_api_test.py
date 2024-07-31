# The purpose of these tests are to ensure the API endpoints responses and status codes are standardized and correct.

import os
from unittest.mock import patch

import pytest

from app.dao.configDataManager import ConfigManager
from app.model.dataModel import MessageModel, RoleEnum
from app.view.appView import AppView


@pytest.fixture
def client():
    # Get the absolute path to the config file
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../storage/config/main_config.yaml'))
    # config_path = '../../storage/config/main_config.yaml'
    config_manager = ConfigManager(config_path)
    flask_app = AppView(config_manager).app
    with flask_app.test_client() as client:
        yield client


def test_sanity_check(client):
    assert True


def test_ask_post_no_message(client):
    response = client.post('/ask', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'No content provided'}


@patch('app.view.appView.AppView.get_current_bot', return_value=lambda api_key: None)
def test_ask_post_no_bot(mock_get_current_bot, client):
    response = client.post('/ask', json={'content': 'Hello'})
    assert response.status_code == 500
    assert response.json == {'error': 'No bot configured or bot unavailable'}


@patch('app.view.appView.AppView.get_current_bot')
@patch('app.view.appView.HistoryManager.add_session_message')
def test_ask_post_success(mock_add_session_message, mock_get_current_bot, client):
    class MockBot:
        def ask(self, message, session):
            return MessageModel(role=RoleEnum.ASSISTANT, content='test')

    mock_get_current_bot.return_value = lambda api_key: MockBot()

    response = client.post('/ask', json={'content': 'Hello'})
    assert response.status_code == 200
    assert response.json == {'response': 'test'}
    mock_add_session_message.assert_called_once()


@patch('app.model.dataModel.SessionModel.serialize', return_value=
dict(id='1',
     time_created='2022-01-01 00:00:00',
     message_list=[],
     vector_store_id='null'))
def test_session_get_success(mock_serialize, client):
    response = client.get('/session')
    assert response.status_code == 200
    assert response.json == {'id': '1',
                             'time_created': '2022-01-01 00:00:00',
                             'message_list': [],
                             'vector_store_id': 'null'}


def test_session_put_no_json(client):
    response_empty_json = client.put('/session')
    assert response_empty_json.status_code == 415


def test_session_put_invalid_json(client):
    error_message = {'status': 'failure', 'message': 'Entry not updated'}
    response_empty_json = client.put('/session', json={})
    assert response_empty_json.status_code == 400
    assert response_empty_json.json == error_message
    response_no_role_name = client.put('/session', json={'content': 'Hello'})
    assert response_no_role_name.status_code == 400
    assert response_no_role_name.json == error_message
    response_no_content = client.put('/session', json={'role_name': 'user'})
    assert response_no_content.status_code == 400
    assert response_no_content.json == error_message


@patch('app.view.appView.HistoryManager.add_session_message', return_value=True)
def test_session_put_add_success(mock_add_session_message, client):
    response = client.put('/session', json={'content': 'test', 'role_name': 'user'})
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Entry updated'}
    mock_add_session_message.assert_called_once()


@patch('app.view.appView.HistoryManager.add_session_message', return_value=False)
def test_session_put_add_failure(mock_add_session_message, client):
    response = client.put('/session', json={'content': 'test', 'role_name': 'user'})
    assert response.status_code == 400
    assert response.json == {'status': 'failure', 'message': 'Entry not updated'}
    mock_add_session_message.assert_called_once()


def test_session_delete_no_json(client):
    response_empty_json = client.delete('/session')
    assert response_empty_json.status_code == 415


def test_session_delete_invalid_json(client):
    error_message = {'status': 'failure', 'message': 'Entry not deleted'}
    response_empty_json = client.delete('/session', json={})
    assert response_empty_json.status_code == 400
    assert response_empty_json.json == error_message
    response_no_message_id = client.delete('/session', json={'content': 'Hello'})
    assert response_no_message_id.status_code == 400
    assert response_no_message_id.json == error_message


@patch('app.view.appView.HistoryManager.delete_session_message', return_value=True)
def test_session_delete_success(mock_delete_session_message, client):
    response = client.delete('/session', json={'message_id': '1'})
    assert response.status_code == 200
    assert response.json == {'status': 'success', 'message': 'Entry deleted'}
    mock_delete_session_message.assert_called_once()


@patch('app.view.appView.HistoryManager.delete_session_message', return_value=False)
def test_session_delete_failure(mock_delete_session_message, client):
    response = client.delete('/session', json={'message_id': '1'})
    assert response.status_code == 400
    assert response.json == {'status': 'failure', 'message': 'Entry not deleted'}
    mock_delete_session_message.assert_called_once()


def test_history_get_success(client):
    response = client.get('/history')
    assert response.status_code == 200
    assert isinstance(response.json, list)


# The following tests are working, but certain parts of the code are not being tested
# Passing these ensures general functionality
# I am unsure how to mock the HistoryManager and ConfigManager methods properly

# ModuleNotFoundError: No module named 'app.view.appView.HistoryManager'; 'app.view.appView' is not a package
# Unable to mock the configManager.config.runtime.current_session_id either
# Unsure why when mocking the HistoryManager methods it is not found when it worked fine in other tests

# @patch('app.view.appView.HistoryManager.create_session', return_value=SessionModel(id='1', time_created='2022-01-01 00:00:00', message_list=[], vector_store_id='null'))
# @patch('app.view.appView.HistoryManager.history.session_id_list', new_callable=list)
# @patch('app.view.appView.ConfigManager.config.runtime.current_session_id', new_callable=str)
# def test_history_put_success(mock_current_session_id, mock_session_id_list, mock_create_session, client):
#     response = client.put('/history')
#     assert response.status_code == 200
#     assert response.json == '1'
#     mock_create_session.assert_called_once()
#     assert mock_session_id_list == ['1']
#     assert mock_current_session_id == '1'

def test_history_delete_no_json(client):
    response_empty_json = client.delete('/history')
    assert response_empty_json.status_code == 415


def test_history_delete_invalid_json(client):
    response_empty_json = client.delete('/history', json={})
    assert response_empty_json.status_code == 400
    response_no_session_id = client.delete('/history', json={'content': 'test'})
    assert response_no_session_id.status_code == 400


@patch('app.view.appView.HistoryManager.delete_session', return_value=True)
def test_history_delete_session_success(mock_delete_session, client):
    response = client.delete('/history', json={'session_id': '1'})
    assert response.status_code == 200
    mock_delete_session.assert_called_once()


@patch('app.view.appView.HistoryManager.delete_session', return_value=False)
def test_history_delete_session_failure(mock_delete_session, client):
    response = client.delete('/history', json={'session_id': '1'})
    assert response.status_code == 400
    mock_delete_session.assert_called_once()


# The following two tests assumes return value is a string (and it probably should be)
# and the existing implementation of this endpoint may have side effects
@patch('app.view.appView.get_nested_attribute', return_value='test')
def test_config_get_success(mock_get_nested_attribute, client):
    response = client.get('/config/test')
    assert response.status_code == 200
    assert response.json == {'test': 'test'}


@patch('app.view.appView.get_nested_attribute', return_value=None)
def test_config_get_not_found(mock_get_nested_attribute, client):
    response = client.get('/config/invalid')
    assert response.status_code == 404
    assert response.json == {'error': 'Configuration key not found'}


def test_config_post_no_json(client):
    response_empty_json = client.post('/config/test')
    assert response_empty_json.status_code == 415


def test_config_post_invalid_json(client):
    response_empty_json = client.post('/config/test', json={})
    assert response_empty_json.status_code == 400
    response_no_value = client.post('/config/test', json={'key': 'value'})
    assert response_no_value.status_code == 400


# These two tests also have problems with mocking the config_manager method
# The functional tests for these cases are done elsewhere

# @patch('app.view.appView.set_nested_attribute', return_value=None)
# @patch('app.view.appView.AppView.config_manager.save', return_value=True)
# def test_config_post_success(mock_set_nested_atrribute, mock_save, client):
#     response = client.post('/config/test', json={'value': 'test'})
#     assert response.status_code == 200
#     mock_set_nested_atrribute.assert_called_once()
#     mock_save.assert_called_once()

# @patch('app.view.appView.set_nested_attribute', return_value=None)
# @patch('app.view.appView.AppView.config_manager.save', return_value=False)
# def test_config_post_failure(mock_set_nested_atrribute, mock_save, client):
#     response = client.post('/config/test', json={'value': 'test'})
#     assert response.status_code == 400
#     mock_set_nested_atrribute.assert_called_once()
#     mock_save.assert_called_once()

def test_bot_get(client):
    response = client.get('/bots')
    assert response.status_code == 200
    assert isinstance(response.json, list)
