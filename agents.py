from abc import ABC, abstractmethod
from typing import Union, Optional, List

from langchain import hub
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents import AgentType
from langchain_core.memory import Memory
from langchain_core.handlers import CallbackHandler
from langchain_core.models import LanguageModel, ChatModel
from langchain_core.prompts import CustomPrompt
from langchain_core.utilities import Tool


class TourAssistant(ABC):
    """
    Abstract base class representing the structure of a tour planning assistant agent.
    """

    @abstractmethod
    def __init__(self, model: Union[LanguageModel, ChatModel], memory: Memory, agent_type: AgentType,
                 verbose: bool) -> None:
        """
        Initializes essential components for a tour assistant.

        Args:
            model (Union[LanguageModel, ChatModel]): The main language model or chat model.
            memory (Memory): Agent memory for tracking interactions.
            agent_type (AgentType): Specifies the type of agent.
            verbose (bool): Enable detailed logging for debugging.

        """
        self.model = model
        self.memory = memory
        self.agent_type = agent_type
        self.tools: List[Tool] = []
        self.verbose = verbose
        self.custom_prompt = None

    @abstractmethod
    def fetch_memory_template(self) -> Optional[str]:
        """
        Retrieves the current memory prompt template, if available.

        Returns:
            Optional[str]: The memory prompt template.

        """
        pass

    @abstractmethod
    def update_memory_template(self, template: str) -> None:
        """
        Sets or modifies the memory prompt template.

        Args:
            template (str): The new memory prompt template.

        """
        pass

    @abstractmethod
    def fetch_agent_template(self) -> Optional[CustomPrompt]:
        """
        Retrieves the existing prompt template for the agent, if available.

        Returns:
            Optional[CustomPrompt]: The agent’s prompt template.

        """
        pass

    @abstractmethod
    def update_agent_template(self, template: str) -> None:
        """
        Sets or modifies the agent prompt template.

        Args:
            template (str): The new agent prompt template.

        """
        pass

    @abstractmethod
    def process_request(self, user_input: str) -> str:
        """
        Processes a request by the user and generates a response.

        Args:
            user_input (str): The user’s query or instruction.

        Returns:
            str: The generated response.

        """
        pass

    @abstractmethod
    def append_tool(self, tool: Tool):
        """
        Adds a new tool to the agent's toolkit.

        Args:
            tool (Tool): Tool to enhance agent’s capabilities.

        """
        pass

    @abstractmethod
    def reset_memory(self) -> None:
        """
        Clears all stored memory for the agent.

        """
        pass


class AdvancedTravelAgent(TourAssistant):
    """
    Implementation of a specialized tour planning agent using advanced memory and language model features.
    """

    def __init__(self, model: Union[LanguageModel, ChatModel], memory: Memory, agent_type: AgentType, verbose: bool,
                 handler: CallbackHandler) -> None:
        """
        Initialize the Advanced Travel Assistant with specific language model and memory.

        Args:
            model (Union[LanguageModel, ChatModel]): The main language or chat model.
            memory (Memory): Memory for interaction tracking.
            agent_type (AgentType): Defines the agent type.
            verbose (bool): Enable detailed output.
            handler (CallbackHandler): Handler for callback functions.

        """
        super().__init__(model, memory, agent_type, verbose)
        self.custom_prompt = hub.load("agent_prompts/advanced_travel")
        self.handler = handler

    def fetch_memory_template(self) -> str:
        """
        Retrieves the memory prompt template associated with this agent.

        Returns:
            str: The memory prompt template.

        """
        return self.memory.get_prompt_template()

    def update_memory_template(self, template: str) -> None:
        """
        Updates the memory prompt template.

        Args:
            template (str): New memory prompt template.

        """
        self.memory.set_prompt_template(template)

    def fetch_agent_template(self) -> CustomPrompt:
        """
        Gets the current agent prompt template.

        Returns:
            CustomPrompt: The agent's prompt template.

        """
        return self.custom_prompt

    def update_agent_template(self, template: str) -> None:
        """
        Sets a new prompt template for the agent.

        Args:
            template (str): The new prompt template.

        """
        self.custom_prompt = CustomPrompt(template)

    def process_request(self, user_input: str) -> str:
        """
        Handles the user’s request, generating a response.

        Args:
            user_input (str): User-provided text.

        Returns:
            str: The agent's response.

        """
        agent = initialize_agent(
            tools=self.tools, 
            model=self.model, 
            prompt=self.custom_prompt,
            memory=self.memory
        )
        executor = AgentExecutor(agent=agent, tools=self.tools, verbose=self.verbose, memory=self.memory)
        inputs = {"query": user_input}
        inputs.update(self.memory.retrieve_memory({}))
        response = executor.invoke(inputs, {"callbacks": [self.handler]})['result']
        return response

    def append_tool(self, tool: Tool) -> None:
        """
        Adds a new tool to the assistant’s toolkit.

        Args:
            tool (Tool): Tool to support additional features.

        """
        self.tools.append(tool)

    def reset_memory(self) -> None:
        """
        Clears agent memory entirely.

        """
        self.memory.clear_data()
