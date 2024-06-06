# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

from azure.ai.assistant.management.assistant_config import AssistantConfig
from azure.ai.assistant.management.async_assistant_client_callbacks import AsyncAssistantClientCallbacks
from azure.ai.assistant.management.async_message import AsyncConversationMessage
from azure.ai.assistant.management.text_message import TextMessage
from azure.ai.assistant.management.base_chat_assistant_client import BaseChatAssistantClient
from azure.ai.assistant.management.exceptions import EngineError, InvalidJSONError
from azure.ai.assistant.management.logger_module import logger

from openai import AsyncAzureOpenAI, AsyncOpenAI

from typing import Optional, Union
from datetime import datetime
import json, uuid, yaml
import asyncio
import tiktoken


class AsyncChatAssistantClient(BaseChatAssistantClient):
    """
    A class that manages an chat assistant client.

    Use the `from_json` or `from_config` factory methods to create an instance of this class.

    :param config_json: The configuration data to use to create the chat client.
    :type config_json: str
    :param callbacks: The callbacks to use for the assistant client.
    :type callbacks: Optional[AssistantClientCallbacks]
    :param client_args: Additional keyword arguments for configuring the AI client.
    :type client_args: Dict
    """
    def __init__(
            self, 
            config_json: str,
            callbacks: Optional[AsyncAssistantClientCallbacks] = None,
            **client_args
    ) -> None:
        super().__init__(config_json, callbacks, async_mode=True, **client_args)
        self._async_client : Union[AsyncOpenAI, AsyncAzureOpenAI] = self._ai_client
        # Init with base settings, leaving async init for the factory method

    async def _async_init(
            self, 
            is_create: bool, 
            timeout: Optional[float]
    ):
        """
        An asynchronous initialization method that loads and sets up the assistant configuration.

        :param is_create: A flag to indicate if the assistant client is being created.
        :type is_create: bool
        :param timeout: The HTTP request timeout in seconds.
        :type timeout: Optional[float]
        """
        await asyncio.to_thread(self._init_chat_assistant_client, self._config_data, is_create, timeout=timeout)

    @classmethod
    async def from_json(
        cls,
        config_json: str,
        callbacks: Optional[AsyncAssistantClientCallbacks] = None,
        timeout: Optional[float] = None,
        **client_args
    ) -> "AsyncChatAssistantClient":
        """
        Creates a AsyncChatAssistantClient instance from JSON configuration data.

        :param config_json: JSON string containing the configuration for the chat assistant.
        :type config_json: str
        :param callbacks: Optional callbacks for the chat assistant client.
        :type callbacks: Optional[AsyncAssistantClientCallbacks]
        :param timeout: Optional timeout for HTTP requests.
        :type timeout: Optional[float]
        :param client_args: Additional keyword arguments for configuring the AI client.
        :type client_args: Dict

        :return: An instance of AsyncChatAssistantClient.
        :rtype: AsyncChatAssistantClient
        """
        try:
            instance = cls(config_json, callbacks, **client_args)
            config_data = json.loads(config_json)
            is_create = not ("assistant_id" in config_data and config_data["assistant_id"])
            await instance._async_init(is_create, timeout)  # Perform async initialization
            return instance
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            raise InvalidJSONError(f"Invalid JSON format: {e}")

    @classmethod
    async def from_yaml(
        cls,
        config_yaml: str,
        callbacks: Optional[AsyncAssistantClientCallbacks] = None,
        timeout: Optional[float] = None,
        **client_args
    ) -> "AsyncChatAssistantClient":
        """
        Creates an AsyncChatAssistantClient instance from YAML configuration data.

        :param config_yaml: YAML string containing the configuration for the chat assistant.
        :type config_yaml: str
        :param callbacks: Optional callbacks for the chat assistant client.
        :type callbacks: Optional[AsyncAssistantClientCallbacks]
        :param timeout: Optional timeout for HTTP requests.
        :type timeout: Optional[float]
        :param client_args: Additional keyword arguments for configuring the AI client.
        :type client_args: Dict

        :return: An instance of AsyncChatAssistantClient.
        :rtype: AsyncChatAssistantClient
        """
        try:
            config_data = yaml.safe_load(config_yaml)
            config_json = json.dumps(config_data)
            return await cls.from_json(config_json, callbacks, timeout, **client_args)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML format: {e}")
            raise EngineError(f"Invalid YAML format: {e}")

    @classmethod
    async def from_config(
        cls,
        config: AssistantConfig,
        callbacks: Optional[AsyncAssistantClientCallbacks] = None,
        timeout: Optional[float] = None,
        **client_args
    ) -> "AsyncChatAssistantClient":
        """
        Creates a AsyncChatAssistantClient instance from an AssistantConfig object.

        :param config: AssistantConfig object containing the configuration for the chat assistant.
        :type config: AssistantConfig
        :param callbacks: Optional callbacks for the chat assistant client.
        :type callbacks: Optional[AsyncAssistantClientCallbacks]
        :param timeout: Optional timeout for HTTP requests.
        :type timeout: Optional[float]
        :param client_args: Additional keyword arguments for configuring the AI client.
        :type client_args: Dict

        :return: An instance of AsyncChatAssistantClient.
        :rtype: AsyncChatAssistantClient
        """
        try:
            config_json = config.to_json()
            return await cls.from_json(config_json, callbacks, timeout, **client_args)
        except Exception as e:
            logger.error(f"Failed to create chat client from config: {e}")
            raise EngineError(f"Failed to create chat client from config: {e}")

    async def purge(
            self,
            timeout: Optional[float] = None
    )-> None:
        """
        Purges the chat assistant from the local configuration.

        :param timeout: The HTTP request timeout in seconds.
        :type timeout: Optional[float]

        :return: None
        :rtype: None
        """
        await asyncio.to_thread(self._purge, timeout)

    async def process_messages(
            self, 
            thread_name: Optional[str] = None,
            user_request: Optional[str] = None,
            additional_instructions: Optional[str] = None,
            timeout: Optional[float] = None,
            stream: Optional[bool] = False
    ) -> Optional[str]:
        """
        Process the messages in given thread.

        :param thread_name: The name of the thread to process.
        :type thread_name: Optional[str]
        :param user_request: The user request to process.
        :type user_request: Optional[str]
        :param additional_instructions: Additional instructions to provide to the assistant.
        :type additional_instructions: Optional[str]
        :param timeout: The HTTP request timeout in seconds.
        :type timeout: Optional[float]
        :param stream: A flag to indicate if the response should be streamed.
        :type stream: Optional[bool]

        :return: The response from the assistant.
        :rtype: Optional[str]
        """
        # Ensure at least one of thread_name or user_request is provided
        if thread_name is None and user_request is None:
            raise ValueError("Either thread_name or user_request must be provided.")

        try:
            logger.info(f"Process messages for chat assistant")
            enc = tiktoken.encoding_for_model(self._assistant_config.model)

            if additional_instructions:
                self._messages.append({"role": "system", "content": additional_instructions})

            if thread_name:
                max_text_messages = self._assistant_config.text_completion_config.max_text_messages if self._assistant_config.text_completion_config else None
                conversation = await self._conversation_thread_client.retrieve_conversation(thread_name=thread_name, max_text_messages=max_text_messages)
                for message in reversed(conversation.messages):
                    if message.role == "user":
                        self._messages.append({"role": "user", "content": message.text_message.content})
                    if message.role == "assistant":
                        self._messages.append({"role": "assistant", "content": message.text_message.content})
            elif user_request:
                self._messages.append({"role": "user", "content": user_request})
                self._token_count += len(enc.encode(user_request))
            
            await self._update_token_count(enc)

            # call the start_run callback
            run_start_time = str(datetime.now())
            run_id = str(uuid.uuid4())
            if thread_name:
                conversation = await self._conversation_thread_client.retrieve_conversation(thread_name)
                user_request = conversation.get_last_text_message("user").content
            await self._callbacks.on_run_start(self._name, run_id, run_start_time, user_request)

            continue_processing = True
            if self._cancel_run_requested.is_set():
                self._cancel_run_requested.clear()

            response = None
            while continue_processing:

                if self._cancel_run_requested.is_set():
                    logger.info("User input processing cancellation requested.")
                    self._cancel_run_requested.clear()
                    break

                text_completion_config = self._assistant_config.text_completion_config

                temperature = None if text_completion_config is None else text_completion_config.temperature
                seed = None if text_completion_config is None else text_completion_config.seed
                frequency_penalty = None if text_completion_config is None else text_completion_config.frequency_penalty
                max_tokens = None if text_completion_config is None else text_completion_config.max_tokens
                presence_penalty = None if text_completion_config is None else text_completion_config.presence_penalty
                top_p = None if text_completion_config is None else text_completion_config.top_p
                response_format = None if text_completion_config is None else {'type': text_completion_config.response_format}

                response = await self._async_client.chat.completions.create(
                    model=self._assistant_config.model,
                    messages=self._messages,
                    tools=self._tools,
                    tool_choice=None if self._tools is None else "auto",
                    stream=stream,
                    temperature=temperature,
                    seed=seed,
                    frequency_penalty=frequency_penalty,
                    max_tokens=max_tokens,
                    presence_penalty=presence_penalty,
                    response_format=response_format,
                    top_p=top_p,
                    timeout=timeout
                )

                if response and stream:
                    continue_processing = await self._handle_streaming_response(response, thread_name, run_id)
                elif response:
                    continue_processing = await self._handle_non_streaming_response(response, thread_name, run_id)
                else:
                    # If there's no response, stop the loop
                    continue_processing = False

            # Reset the system messages
            self._reset_system_messages(self._assistant_config)

            await self._callbacks.on_run_update(self._name, run_id, "completed", thread_name)

            run_end_time = str(datetime.now())
            if not thread_name and not stream:
                # If there's no thread name, call the end_run callback and return the response
                response_message = response.choices[0].message.content
                await self._callbacks.on_run_end(self._name, run_id, run_end_time, thread_name, response_message)
                return response_message

            await self._callbacks.on_run_end(self._name, run_id, run_end_time, thread_name)

        except Exception as e:
            logger.error(f"Error occurred during processing run: {e}")
            raise EngineError(f"Error occurred during processing run: {e}")

    async def _handle_non_streaming_response(self, response, thread_name, run_id):
        response_message = response.choices[0].message
        self._messages.append(response_message)

        if response_message.content:
            # extend conversation with assistant's reply
            if thread_name:
                await self._conversation_thread_client.create_conversation_thread_message(
                    response_message.content,
                    thread_name,
                    metadata={"chat_assistant": self._name}
                )
            return False

        tool_calls = response_message.tool_calls
        if tool_calls != None:
            for tool_call in tool_calls:
                function_response = await asyncio.to_thread(
                    self._handle_function_call, 
                    tool_call.function.name, 
                    tool_call.function.arguments
                )
                await self._callbacks.on_function_call_processed(self._name, run_id, tool_call.function.name, tool_call.function.arguments, str(function_response))
                self._messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_call.function.name,
                        "content": function_response,
                    }
                )
            return True

    async def _handle_streaming_response(self, response, thread_name, run_id):
        tool_calls, collected_messages = await self._process_response_chunks(response, thread_name, run_id)
        await self._process_tool_calls(tool_calls, run_id)
        await self._update_conversation_with_messages(collected_messages, thread_name)
        return bool(tool_calls)  # Return True if there were tool calls processed, otherwise False

    async def _process_response_chunks(self, response, thread_name, run_id):
        tool_calls = []
        collected_messages = []
        is_first_message = True

        async for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                message : AsyncConversationMessage = await AsyncConversationMessage.create(self.ai_client, None)
                message.text_message = TextMessage(delta.content)
                await self._callbacks.on_run_update(self._name, run_id, "streaming", thread_name, is_first_message, message)
                collected_messages.append(delta.content)
                is_first_message = False
            if delta and delta.tool_calls:
                tool_calls = await asyncio.to_thread(self._append_tool_calls, tool_calls, delta.tool_calls)

        return tool_calls, collected_messages

    async def _process_tool_calls(self, tool_calls, run_id):
        if tool_calls:
            logger.info(f"Tool calls: {tool_calls}")
            self._messages.append({
                "tool_calls": tool_calls,
                "role": 'assistant',
            })
    
        for tool_call in tool_calls:
            function_response = await asyncio.to_thread(
                self._handle_function_call, 
                tool_call['function']['name'], 
                tool_call['function']['arguments']
            )
            await self._callbacks.on_function_call_processed(
                self._name, run_id, 
                tool_call['function']['name'], 
                tool_call['function']['arguments'], 
                str(function_response)
            )

            # Appending the processed tool call and its response to self._messages
            self._messages.append({
                "tool_call_id": tool_call['id'],
                "role": "tool",
                "name": tool_call['function']['name'],
                "content": str(function_response),  # Ensure content is stringified if necessary
            })

    async def _update_conversation_with_messages(self, collected_messages, thread_name):
        full_response = ''.join(filter(None, collected_messages))
        if full_response and thread_name:
            await self._conversation_thread_client.create_conversation_thread_message(
                message=full_response, 
                thread_name=thread_name, 
                metadata={"chat_assistant": self._name}
            )
            logger.info("Messages updated in conversation.")

    async def _update_token_count(self, encoder : tiktoken.Encoding):
        '''
        Clear older messages from the message thread to keep the overall token count below the limit, preserves conversation context.

        '''

        if self._token_count > self._assistant_config.model_conv_token_limit:
            while self._token_count > self._assistant_config.model_conv_token_limit:
                oldest_message = self._messages[0]
                if oldest_message['role'] == 'user' or oldest_message['role'] == 'assistant':
                    self._token_count -= len(encoder.encode(oldest_message['content']))
                    logger.info(f"{self._assistant_config.model_conv_token_limit} token count exceeded, removing oldest message from messages: {oldest_message['content']}")
                    self._messages.remove(oldest_message)

        

        
