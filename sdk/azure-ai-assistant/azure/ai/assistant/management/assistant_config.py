# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

from azure.ai.assistant.management.function_config import FunctionConfig
from azure.ai.assistant.management.logger_module import logger

import json, os
from typing import Optional, Union

class ModelMaxTokens:
    def __init__(self):
        self.model_token_limits = {
            "gpt-4o": 128000,
            "gpt-3": 2048,
            "gpt-4": 8192,
        }

class TextCompletionConfig:
    """
    A class representing the configuration for text completion.

    :param frequency_penalty: The frequency penalty.
    :type frequency_penalty: float
    :param max_tokens: The maximum number of tokens.
    :type max_tokens: int
    :param presence_penalty: The presence penalty.
    :type presence_penalty: float
    :param response_format: The response format.
    :type response_format: str
    :param temperature: The temperature.
    :type temperature: float
    :param top_p: The top p.
    :type top_p: float
    :param seed: The seed.
    :type seed: Optional[int]
    :param max_text_messages: The maximum number of text messages.
    :type max_text_messages: Optional[int]
    """
    def __init__(self, 
                 frequency_penalty: float, 
                 max_tokens: int, 
                 presence_penalty: float,
                 response_format: str,
                 temperature: float, 
                 top_p: float,
                 seed: Optional[int] = None,
                 max_text_messages: Optional[int] = None
        ) -> None:
        self._frequency_penalty = frequency_penalty
        self._max_tokens = max_tokens
        self._presence_penalty = presence_penalty
        self._response_format = response_format
        self._temperature = temperature
        self._top_p = top_p
        self._seed = seed
        self._max_text_messages = max_text_messages

    def to_dict(self):
        return {
            'frequency_penalty': self.frequency_penalty,
            'max_tokens': self.max_tokens,
            'presence_penalty': self.presence_penalty,
            'response_format': self.response_format,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'seed': self.seed,
            'max_text_messages': self.max_text_messages
        }

    @property
    def frequency_penalty(self) -> float:
        """
        Get the frequency penalty.

        :return: The frequency penalty.
        :rtype: float
        """
        return self._frequency_penalty
    
    @frequency_penalty.setter
    def frequency_penalty(self, value) -> None:
        """
        Set the frequency penalty.

        :param value: The frequency penalty.
        :type value: float
        """
        self._frequency_penalty = value

    @property
    def max_tokens(self) -> int:
        """
        Get the maximum number of tokens.

        :return: The maximum number of tokens.
        :rtype: int
        """
        return self._max_tokens
    
    @max_tokens.setter
    def max_tokens(self, value) -> None:
        """
        Set the maximum number of tokens.

        :param value: The maximum number of tokens.
        :type value: int
        """
        self._max_tokens = value

    @property
    def presence_penalty(self) -> float:
        """
        Get the presence penalty.

        :return: The presence penalty.
        :rtype: float
        """
        return self._presence_penalty
    
    @presence_penalty.setter
    def presence_penalty(self, value) -> None:
        """
        Set the presence penalty.

        :param value: The presence penalty.
        :type value: float
        """
        self._presence_penalty = value

    @property
    def response_format(self) -> str:
        """
        Get the response format.

        :return: The response format.
        :rtype: str
        """
        return self._response_format
    
    @response_format.setter
    def response_format(self, value) -> None:
        """
        Set the response format.

        :param value: The response format.
        :type value: str
        """
        self._response_format = value

    @property
    def temperature(self) -> float:
        """
        Get the temperature.

        :return: The temperature.
        :rtype: float
        """
        return self._temperature
    
    @temperature.setter
    def temperature(self, value) -> None:
        """
        Set the temperature.

        :param value: The temperature.
        :type value: float
        """
        self._temperature = value

    @property
    def top_p(self) -> float:
        """
        Get the top p.

        :return: The top p.
        :rtype: float
        """
        return self._top_p
    
    @top_p.setter
    def top_p(self, value) -> None:
        """
        Set the top p.

        :param value: The top p.
        :type value: float
        """
        self._top_p = value

    @property
    def seed(self) -> Optional[int]:
        """
        Get the seed.

        :return: The seed.
        :rtype: Optional[int]
        """
        return self._seed
    
    @seed.setter
    def seed(self, value) -> None:
        """
        Set the seed.

        :param value: The seed.
        :type value: Optional[int]
        """
        self._seed = value

    @property
    def max_text_messages(self) -> Optional[int]:
        """
        Get the maximum number of text messages.

        :return: The maximum number of text messages.
        :rtype: Optional[int]
        """
        return self._max_text_messages
    
    @max_text_messages.setter
    def max_text_messages(self, value) -> None:
        """
        Set the maximum number of text messages.

        :param value: The maximum number of text messages.
        :type value: Optional[int]
        """
        self._max_text_messages = value


class AssistantTextCompletionConfig:
    """
    A class representing the configuration for assistant text completion.

    :param temperature: The temperature.
    :type temperature: float
    :param max_completion_tokens: The maximum number of completion tokens.
    :type max_completion_tokens: int
    :param max_prompt_tokens: The maximum number of prompt tokens.
    :type max_prompt_tokens: int
    :param top_p: The top p.
    :type top_p: float
    :param response_format: The response format.
    :type response_format: str
    :param truncation_strategy: The truncation strategy.
    :type truncation_strategy: dict
    """
    def __init__(self, 
                 temperature: float, 
                 max_completion_tokens: int,
                 max_prompt_tokens: int,
                 top_p: float, 
                 response_format: str,
                 truncation_strategy : dict
    ) -> None:
        self._temperature = temperature
        self._max_completion_tokens = max_completion_tokens
        self._max_prompt_tokens = max_prompt_tokens
        self._top_p = top_p
        self._response_format = response_format
        self._truncation_strategy = truncation_strategy

    def to_dict(self):
        return {'temperature': self.temperature,
                'max_completion_tokens': self.max_completion_tokens,
                'max_prompt_tokens': self.max_prompt_tokens,
                'top_p': self.top_p,
                'response_format': self.response_format,
                'truncation_strategy': self.truncation_strategy
                }

    @property
    def temperature(self) -> float:
        """
        Get the temperature.

        :return: The temperature.
        :rtype: float
        """
        return self._temperature
    
    @temperature.setter
    def temperature(self, value) -> None:
        """
        Set the temperature.

        :param value: The temperature.
        :type value: float
        """
        self._temperature = value

    @property
    def max_completion_tokens(self) -> int:
        """
        Get the maximum number of completion tokens.

        :return: The maximum number of completion tokens.
        :rtype: int
        """
        return self._max_completion_tokens
    
    @max_completion_tokens.setter
    def max_completion_tokens(self, value) -> None:
        """
        Set the maximum number of completion tokens.

        :param value: The maximum number of completion tokens.
        :type value: int
        """
        self._max_completion_tokens = value

    @property
    def max_prompt_tokens(self) -> int:
        """
        Get the maximum number of prompt tokens.

        :return: The maximum number of prompt tokens.
        :rtype: int
        """
        return self._max_prompt_tokens
    
    @max_prompt_tokens.setter
    def max_prompt_tokens(self, value) -> None:
        """
        Set the maximum number of prompt tokens.

        :param value: The maximum number of prompt tokens.
        :type value: int
        """
        self._max_prompt_tokens = value

    @property
    def top_p(self) -> float:
        """
        Get the top p.

        :return: The top p.
        :rtype: float
        """
        return self._top_p
    
    @top_p.setter
    def top_p(self, value) -> None:
        """
        Set the top p.

        :param value: The top p.
        :type value: float
        """
        self._top_p = value

    @property
    def response_format(self) -> str:
        """
        Get the response format.

        :return: The response format.
        :rtype: str
        """
        return self._response_format
    
    @response_format.setter
    def response_format(self, value) -> None:
        """
        Set the response format.

        :param value: The response format.
        :type value: str
        """
        self._response_format = value

    @property
    def truncation_strategy(self) -> dict:
        """
        Get the truncation strategy.

        :return: The truncation strategy.
        :rtype: dict
        """
        return self._truncation_strategy
    
    @truncation_strategy.setter
    def truncation_strategy(self, value) -> None:
        """
        Set the truncation strategy.

        :param value: The truncation strategy.
        :type value: dict
        """
        self._truncation_strategy = value


class VectorStoreConfig:
    """
    A class representing the configuration for a vector store.

    :param name: The name of the vector store.
    :type name: str
    :param id: The ID of the vector store.
    :type id: str
    :param files: The files.
    :type files: dict
    :param metadata: The metadata.
    :type metadata: dict
    :param expires_after: The expiration time.
    :type expires_after: dict
    """
    def __init__(self,
                 name : str,
                 id : str = None,
                 files : dict = None,
                 metadata : dict = None,
                 expires_after : dict = None
    ):
        self._name = name
        self._id = id
        self._files = files
        self._metadata = metadata
        self._expires_after = expires_after

    def __eq__(self, other):
        if not isinstance(other, VectorStoreConfig):
            return NotImplemented

        return (self.name == other.name and
                self.id == other.id and
                self.files == other.files and
                self.metadata == other.metadata and
                self.expires_after == other.expires_after)

    def to_dict(self) -> dict:
        """
        Convert the vector store configuration to a dictionary.

        :return: The vector store configuration as a dictionary.
        :rtype: dict
        """
        return {
            'name': self.name,
            'id': self.id,
            'files': self.files,
            'metadata': self.metadata,
            'expires_after': self.expires_after
        }

    @property
    def name(self) -> str:
        """
        Get the name.

        :return: The name.
        :rtype: str
        """
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Set the name.

        :param value: The name.
        :type value: str
        """
        self._name = value

    @property
    def id(self) -> str:
        """
        Get the ID.

        :return: The ID.
        :rtype: str
        """
        return self._id
    
    @id.setter
    def id(self, value):
        """
        Set the ID.

        :param value: The ID.
        :type value: str
        """
        self._id = value

    @property
    def files(self) -> dict:
        """
        Get the files.

        :return: The files.
        :rtype: dict
        """
        return self._files
    
    @files.setter
    def files(self, value):
        """
        Set the files.

        :param value: The files.
        :type value: dict
        """
        self._files = value

    @property
    def metadata(self) -> dict:
        """
        Get the metadata.

        :return: The metadata.
        :rtype: dict
        """
        return self._metadata
    
    @metadata.setter
    def metadata(self, value):
        """
        Set the metadata.

        :param value: The metadata.
        :type value: dict
        """
        self._metadata = value

    @property
    def expires_after(self) -> dict:
        """
        Get the expiration time.

        :return: The expiration time.
        :rtype: dict
        """
        return self._expires_after
    
    @expires_after.setter
    def expires_after(self, value):
        """
        Set the expiration time.

        :param value: The expiration time.
        :type value: dict
        """
        self._expires_after = value


class ToolResourcesConfig:
    """
    A class representing the configuration for tool resources.

    :param code_interpreter_files: The code interpreter files.
    :type code_interpreter_files: dict
    :param file_search_vector_stores: The file search vector stores.
    :type file_search_vector_stores: list[VectorStoreConfig]
    """
    def __init__(self, 
                 code_interpreter_files : dict = None,
                 file_search_vector_stores : list[VectorStoreConfig] = None):

        self._code_interpreter_files = code_interpreter_files
        self._file_search_vector_stores = file_search_vector_stores

    def __eq__(self, other):
        if not isinstance(other, ToolResourcesConfig):
            return NotImplemented

        return (self.code_interpreter_files == other.code_interpreter_files and
                self.file_search_vector_stores == other.file_search_vector_stores)

    def to_dict(self) -> dict:
        """
        Convert the tool resources configuration to a dictionary.

        :return: The tool resources configuration as a dictionary.
        :rtype: dict
        """
        return {
            'code_interpreter': {
                'files': self.code_interpreter_files
            },
            'file_search': {
                'vector_stores': [vs.to_dict() for vs in self.file_search_vector_stores] if self.file_search_vector_stores is not None else None
            }
        }
    
    @property
    def code_interpreter_files(self):
        """
        Get the code interpreter files.

        :return: The code interpreter files.
        :rtype: dict
        """
        return self._code_interpreter_files
    
    @code_interpreter_files.setter
    def code_interpreter_files(self, value):
        """
        Set the code interpreter files.

        :param value: The code interpreter files.
        :type value: dict
        """
        self._code_interpreter_files = value

    @property
    def file_search_vector_stores(self) -> list[VectorStoreConfig]:
        """
        Get the file search vector stores.

        :return: The file search vector stores.
        :rtype: list[VectorStoreConfig]
        """
        return self._file_search_vector_stores
    
    @file_search_vector_stores.setter
    def file_search_vector_stores(self, value):
        """
        Set the file search vector stores.

        :param value: The file search vector stores.
        :type value: list[VectorStoreConfig]
        """
        self._file_search_vector_stores = value


class AssistantConfig:
    """
    A class representing the configuration for an assistant.

    :param config_data: The configuration data for the assistant.
    :type config_data: dict
    """
    def __init__(self, 
                 config_data : dict
    ) -> None:
        self._config_data = config_data
        self._name = config_data['name']
        self._instructions = self._remove_trailing_spaces(config_data['instructions']) if 'instructions' in config_data else ""
        
        # Initialize assistant_id appropriately based on presence and content in config_data
        self._assistant_id = config_data.get('assistant_id', None) if config_data.get('assistant_id', '') != '' else None
        self._ai_client_type = config_data.get('ai_client_type', 'OPEN_AI')
        self._model = config_data['model']
        self._assistant_type = config_data.get('assistant_type', 'assistant')
        self._file_references = config_data.get('file_references', [])
        
        # Extracting tool resources configuration
        self._tool_resources = self._initialize_tool_resources(config_data.get('tool_resources'))

        self._functions = config_data.get('functions', [])
        self._function_configs = self._get_function_configs()
        
        # Manage tool activation based on config_data
        self._file_search = config_data.get('file_search', False)
        self._code_interpreter = config_data.get('code_interpreter', False)
        
        # Set default output folder as absolute path to 'output' folder in current directory
        default_output_folder_path = os.path.join(os.getcwd(), 'output')
        self._output_folder_path = config_data.get('output_folder_path', default_output_folder_path)
        self._assistant_role = config_data.get('assistant_role', 'user')

        # Completion settings based on assistant type
        self._text_completion_config = self._setup_completion_settings(config_data)

        # Config folder for local assistant and threads configuration
        self._config_folder = None

    def _setup_completion_settings(self, config_data):
        if config_data.get('completion_settings', None) is not None:
            if self._assistant_type == 'chat_assistant':
                completion_data = config_data.get('completion_settings', {
                    'frequency_penalty': 0.0,
                    'max_tokens': 1000,
                    'presence_penalty': 0.0,
                    'response_format': 'text',
                    'temperature': 1.0,
                    'top_p': 1.0,
                    'seed': None,
                    'max_text_messages': None,
                })
                # Constructing TextCompletionConfig from the dictionary
                return TextCompletionConfig(
                    frequency_penalty=completion_data['frequency_penalty'],
                    max_tokens=completion_data['max_tokens'],
                    presence_penalty=completion_data['presence_penalty'],
                    response_format=completion_data['response_format'],
                    temperature=completion_data['temperature'],
                    top_p=completion_data['top_p'],
                    seed=None,
                    max_text_messages=completion_data['max_text_messages']
                )
            elif self._assistant_type == 'assistant':
                completion_data = config_data.get('completion_settings', {
                    'temperature': 1.0,
                    'max_completion_tokens': 1000,
                    'max_prompt_tokens': 1000,
                    'top_p': 1.0,
                    'response_format': 'text',
                    'truncation_strategy': {
                        'type': 'auto',
                        'last_messages': None
                    }
                })
                # Constructing AssistantTextCompletionConfig from the dictionary
                return AssistantTextCompletionConfig(
                    temperature=completion_data['temperature'],
                    max_completion_tokens=completion_data['max_completion_tokens'],
                    max_prompt_tokens=completion_data['max_prompt_tokens'],
                    top_p=completion_data['top_p'],
                    response_format=completion_data['response_format'],
                    truncation_strategy=completion_data['truncation_strategy']
                )

    def _initialize_tool_resources(self, tool_resources_data):
        if tool_resources_data:
            code_interpreter_files = tool_resources_data.get('code_interpreter', {}).get('files', {})
            file_search_vector_stores_data = tool_resources_data.get('file_search', {}).get('vector_stores', [])
            
            if file_search_vector_stores_data is not None:
                file_search_vector_stores = [
                    VectorStoreConfig(
                        name=store.get('name'),
                        id=store.get('id'), 
                        files=store.get('files', []), 
                        metadata=store.get('metadata', {}),
                        expires_after=store.get('expires_after', {})
                    ) for store in file_search_vector_stores_data
                ]
            else:
                file_search_vector_stores = None

            return ToolResourcesConfig(
                code_interpreter_files=code_interpreter_files, 
                file_search_vector_stores=file_search_vector_stores
            )
        if self._assistant_type == "chat_assistant":
            return None
        else:
            return ToolResourcesConfig()

    def __eq__(self, other):
        if not isinstance(other, AssistantConfig):
            return NotImplemented

        return (self._name == other._name and
                self.instructions == other.instructions and
                self._assistant_id == other._assistant_id and
                self._ai_client_type == other._ai_client_type and
                self._model == other._model and
                self._file_references == other._file_references and
                self._tool_resources == other._tool_resources and
                self._functions == other._functions and
                self._file_search == other._file_search and
                self._code_interpreter == other._code_interpreter)

    @classmethod
    def from_dict(
        self, 
        config_data : dict
    ) -> 'AssistantConfig':
        """
        Create an AssistantConfig object from a dictionary.

        :param config_data: The configuration data for the assistant.
        :type config_data: dict

        :return: The AssistantConfig object.
        :rtype: AssistantConfig
        """
        return AssistantConfig(config_data)

    def to_json(self) -> str:
        """Return the configuration data as a JSON string.
        
        :return: The configuration data as a JSON string.
        :rtype: str
        """
        try:
            return json.dumps(self._get_config_data(), indent=4)
        except Exception as e:
            logger.error(f"Error converting config to JSON: {e}")
            return None

    def _get_config_data(self):
        self._config_data['name'] = self._name
        self._config_data['instructions'] = self._instructions
        self._config_data['assistant_id'] = self._assistant_id
        self._config_data['ai_client_type'] = self._ai_client_type
        self._config_data['model'] = self._model
        self._config_data['file_references'] = self._file_references
        self._config_data['tool_resources'] = self._tool_resources.to_dict() if self._tool_resources is not None else None
        self._config_data['file_search'] = self._file_search if self._file_search else False
        self._config_data['code_interpreter'] = self._code_interpreter
        self._config_data['functions'] = self._functions
        self._config_data['output_folder_path'] = self._output_folder_path
        self._config_data['assistant_type'] = self._assistant_type
        self._config_data['assistant_role'] = self._assistant_role
        self._config_data['completion_settings'] = self._text_completion_config.to_dict() if self._text_completion_config is not None else None
        self._config_data['config_folder'] = self._config_folder
        return self._config_data

    def _get_function_configs(self):
        function_configs = []
        for function_spec in self._functions:
            function_configs.append(FunctionConfig(function_spec))
        return function_configs
    
    @property
    def name(self) -> str:
        """Get the name.
        
        :return: The name of the assistant.
        :rtype: str
        """
        return self._name

    @property
    def assistant_id(self) -> str:
        """Get the assistant ID.
        
        :return: The assistant ID.
        :rtype: str
        """
        return self._assistant_id

    @assistant_id.setter
    def assistant_id(self, value) -> None:
        """
        Set the assistant ID.
        
        :param value: The assistant ID.
        :type value: str
        """
        self._assistant_id = value

    @property
    def ai_client_type(self) -> str:
        """Get the AI client type.
        
        :return: The AI client type.
        :rtype: str
        """
        return self._ai_client_type

    @ai_client_type.setter
    def ai_client_type(self, value) -> None:
        """
        Set the AI client type.
        
        :param value: The AI client type.
        :type value: str
        """
        self._ai_client_type = value

    @property
    def model(self) -> str:
        """Get the model.
        
        :return: The model.
        :rtype: str
        """
        return self._model
    
    @property
    def model_conv_token_limit(self) -> str:
        """Get the model.
        
        :return: The model.
        :rtype: str
        """
        return ModelMaxTokens().model_token_limits[self._model]
    
    @model.setter
    def model(self, value) -> None:
        """
        Set the model.
        
        :param value: The model.
        :type value: str
        """
        self._model = value

    @property
    def file_references(self) -> list:
        """Get the file references.
        
        :return: The file references.
        :rtype: list
        """
        return self._file_references
    
    @file_references.setter
    def file_references(self, value) -> None:
        """
        Set the file references.
        
        :param value: The file references.
        :type value: list
        """
        self._file_references = value

    @property
    def tool_resources(self) -> ToolResourcesConfig:
        """Get the tool resources.
        
        :return: The tool resources.
        :rtype: ToolResources
        """
        return self._tool_resources

    @tool_resources.setter
    def tool_resources(self, value) -> None:
        """
        Set the tool resources.
        
        :param value: The tool resources.
        :type value: ToolResources
        """
        self._tool_resources = value

    @property
    def file_search(self) -> bool:
        """Get the file search.
        
        :return: The file search.
        :rtype: bool
        """
        return self._file_search

    @file_search.setter
    def file_search(self, value) -> None:
        """
        Set the file search.
        
        :param value: The file search.
        :type value: bool
        """
        self._file_search = value

    @property
    def code_interpreter(self) -> bool:
        """Get the code interpreter.
        
        :return: The code interpreter.
        :rtype: bool
        """
        return self._code_interpreter
    
    @code_interpreter.setter
    def code_interpreter(self, value) -> None:
        """
        Set the code interpreter.
        
        :param value: The code interpreter.
        :type value: bool
        """
        self._code_interpreter = value

    @property
    def functions(self) -> list:
        """Get the functions.
        
        :return: The functions.
        :rtype: list
        """
        return self._functions
    
    @functions.setter
    def functions(self, value) -> None:
        """
        Set the functions.
        
        :param value: The functions.
        :type value: list
        """
        self._functions = value

    @property
    def instructions(self) -> str:
        """Get the instructions.
        
        :return: The instructions.
        :rtype: str
        """
        instructions = self._instructions
        if os.path.isfile(instructions):
            # If it's a file, open and read its content to use as instructions
            with open(instructions, 'r') as file:
                instructions = file.read()
        return instructions

    @instructions.setter
    def instructions(self, value) -> None:
        """
        Set the instructions.
        
        :param value: The instructions.
        :type value: str
        """
        self._instructions = value

    @property
    def output_folder_path(self) -> str:
        """Get the output folder path.
        
        :return: The output folder path.
        :rtype: str
        """
        return self._output_folder_path
    
    @output_folder_path.setter
    def output_folder_path(self, value) -> None:
        """
        Set the output folder path.
        
        :param value: The output folder path.
        :type value: str
        """
        self._output_folder_path = value

    @property
    def assistant_type(self) -> str:
        """Get the assistant type.
        
        :return: The assistant type.
        :rtype: str
        """
        return self._assistant_type
    
    @property
    def assistant_role(self) -> str:
        """Get the assistant role.
        
        :return: The assistant role.
        :rtype: str
        """
        return self._assistant_role

    @property
    def text_completion_config(self) -> Union[TextCompletionConfig, AssistantTextCompletionConfig, None]:
        """Get the text completion config.
        
        :return: The completion config.
        :rtype: Union[TextCompletionConfig, AssistantTextCompletionConfig, None]
        """
        return self._text_completion_config
    
    @property
    def config_folder(self) -> str:
        """Get the config folder.
        
        :return: The config folder.
        :rtype: str
        """
        return self._config_folder
    
    @config_folder.setter
    def config_folder(self, value) -> None:
        """
        Set the config folder.
        
        :param value: The config folder.
        :type value: str
        """
        self._config_folder = value

    def _remove_trailing_spaces(self, text):
        return '\n'.join(line.rstrip() for line in text.splitlines())
