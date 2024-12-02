from openai import OpenAI
import json
import os

from app.model.dataModel import MessageModel, SessionModel, RoleEnum
from app.model.agentModel import AgentModel
from .baseBot import BaseBot
from app.tools import *

our_api_request_forced_a_tool_call = False

def append_to_message(response, messages):
    role, content = response.choices[0].message.role, response.choices[0].message.content
    messages.append(dict(role=role, content=content))

def handle_length_error(response):
    raise NotImplementedError


def handle_content_filter_error(response):
    raise NotImplementedError

def handle_tool_call(response):
    # Iterate through tool calls to handle each weather check
    for tool_call in response.choices[0].message.tool_calls:
        function = FUNCTION_MAPPING.get(tool_call.function.name)
        arguments = json.loads(tool_call.function.arguments)
        function_output = function(**arguments)

        if function_output is None:
            function_output = "N/A"

        tool_output = {
                "role": "tool",
                "tool_call_id": tool_call.id
            }


        if tool_call.function.name == "some_specific_name":
            # need to engineer the output content
            pass
        elif tool_call.function.name == "get_current_weather":
            tool_output["content"] = json.dumps(dict(weather=function_output))
        else:
            tool_output["content"] = json.dumps(function_output)

        # prepend the tool output to the messages list
        return tool_output

def handle_normal_response(response, messages):
    append_to_message(response, messages)
    print("Assistant: " + response.choices[0].message.content)

def handle_unexpected_case(response):
    raise NotImplementedError


class OpenAIBot(BaseBot):
    def __init__(self, api_key: str):
        """
        Initialize the OpenAIBot with the provided API key.

        Args:
            api_key (str): The API key for accessing OpenAI services.
        """
        self.client = OpenAI(api_key=api_key)
        # self.client = OpenAI(  # TODO add support for ollama model
        #     base_url='http://localhost:11434/v1/',
        #     api_key='ollama',
        # )
    def ask(self,
            message: MessageModel,
            session: SessionModel,
            agent: AgentModel,
            force_tool_call: bool = True) -> MessageModel:
        """
        Sends a message to the OpenAI chat completion API and returns the response.

        Args:
            message (MessageModel): The user's message to be sent.
            session (SessionModel): The current session containing the conversation history.
            agent (AgentModel): The agent model.

        Returns:
            MessageModel: The response message from the OpenAI API.
        """
        if agent:
            fake_message = MessageModel(content=agent.generate_prompt(query=message.content),
                                        role=message.role)
        else:
            fake_message = message

        messages = session.serialize()["message_list"] + [fake_message.serialize()]

        while(True):
            response = self.client.chat.completions.create(
                model="gpt-4o",
                # model="llama3.2",# TODO add support for ollama model
                messages=messages,
                tools=TOOLS_DEFINE if force_tool_call else None,
            )

            # Check if the conversation was too long for the context window
            if response.choices[0].finish_reason == "length":
                print("Error: The conversation was too long for the context window.")
                # Handle the error as needed, e.g., by truncating the conversation or asking for clarification
                handle_length_error(response)
                break

            # Check if the model's output included copyright material (or similar)
            if response.choices[0].finish_reason == "content_filter":
                print("Error: The content was filtered due to policy violations.")
                # Handle the error as needed, e.g., by modifying the request or notifying the user
                handle_content_filter_error(response)
                break

            # Check if the model has made a tool_call. This is the case either if the "finish_reason" is "tool_calls" or if the "finish_reason" is "stop" and our API request had forced a function call
            if (response.choices[0].finish_reason == "tool_calls" or
                # This handles the edge case where if we forced the model to call one of our functions, the finish_reason will actually be "stop" instead of "tool_calls"
                (our_api_request_forced_a_tool_call and response.choices[0].finish_reason == "stop")):
                # Handle tool call
                print("Log: Model made a tool call.")
                # Your code to handle tool calls
                tool_output = handle_tool_call(response)
                messages.append(tool_output)
                continue

            # Else finish_reason is "stop", in which case the model was just responding directly to the user
            elif response.choices[0].finish_reason == "stop":
                # Handle the normal stop case
                print("Log: Model responded directly to the user.")
                # Your code to handle normal responses
                handle_normal_response(response, messages)
                break

            # Catch any other case, this is unexpected
            else:
                print("Unexpected finish_reason:", response.choices[0].finish_reason)
                # Handle unexpected cases as needed
                handle_unexpected_case(response)
                break

        # Retrieve the bot's response
        content_response = messages[-1]["content"]

        # Create a new message model for the response
        message_response = MessageModel(content=content_response, role=RoleEnum.ASSISTANT)

        # Return the last assistant message and the updated context
        return message_response

