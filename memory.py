from typing import Dict, Union, List, Any
from langchain.callbacks.base import CallbackHandlerBase
from langchain_core.agents import AgentResult, AgentEvent
from langchain_core.messages import MessageBase
from langchain_core.results import ModelResult
from streamlit.runtime.state import StateProxy

class CustomCallbackHandler(CallbackHandlerBase):
    """
    Custom callback handler for handling events in the language model interactions.
    """

    def __init__(self, session_state: StateProxy) -> None:
        """
        Initializes the callback handler with the session state for Streamlit.

        Args:
            session_state (StateProxy): Streamlit session state to manage app state.

        """
        super(CustomCallbackHandler, self).__init__()
        self.session_state = session_state

    def on_model_start(self, data: Dict[str, Any], prompts: List[str], **extra_args: Any) -> Any:
        """
        Triggered when the language model starts processing.

        Args:
            data (Dict[str, Any]): Serialized data for model configuration.
            prompts (List[str]): Prompt list provided to the model.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_model_start(data, prompts, **extra_args)

    def on_chat_model_initiate(self, data: Dict[str, Any], messages: List[List[MessageBase]], **extra_args: Any) -> Any:
        """
        Triggered when a chat model initiates.

        Args:
            data (Dict[str, Any]): Configuration data.
            messages (List[List[MessageBase]]): List of message objects.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_chat_model_initiate(data, messages, **extra_args)

    def on_model_token_received(self, token: str, **extra_args: Any) -> Any:
        """
        Runs when a new token is received from the model (used when streaming).

        Args:
            token (str): The received token.
            **extra_args (Any): Extra parameters.

        """
        return super(CustomCallbackHandler, self).on_model_token_received(token, **extra_args)

    def on_model_complete(self, result: ModelResult, **extra_args: Any) -> Any:
        """
        Called upon model completion.

        Args:
            result (ModelResult): The model’s result output.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_model_complete(result, **extra_args)

    def on_model_error(self, error: Union[Exception, KeyboardInterrupt], **extra_args: Any) -> Any:
        """
        Triggered on model error.

        Args:
            error (Union[Exception, KeyboardInterrupt]): The error encountered.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_model_error(error, **extra_args)

    def on_chain_initiate(self, data: Dict[str, Any], inputs: Dict[str, Any], **extra_args: Any) -> Any:
        """
        Runs at the beginning of a chain.

        Args:
            data (Dict[str, Any]): Configuration data for the chain.
            inputs (Dict[str, Any]): Input data for the chain.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_chain_initiate(data, inputs, **extra_args)

    def on_chain_complete(self, outputs: Dict[str, Any], **extra_args: Any) -> Any:
        """
        Called when a chain process ends.

        Args:
            outputs (Dict[str, Any]): Outputs from the chain.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_chain_complete(outputs, **extra_args)

    def on_chain_exception(self, error: Union[Exception, KeyboardInterrupt], **extra_args: Any) -> Any:
        """
        Runs when a chain encounters an error.

        Args:
            error (Union[Exception, KeyboardInterrupt]): The exception or error.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_chain_exception(error, **extra_args)

    def on_tool_initiate(self, data: Dict[str, Any], input_text: str, **extra_args: Any) -> Any:
        """
        Triggered when a tool is initiated.

        Args:
            data (Dict[str, Any]): Serialized tool data.
            input_text (str): Input for the tool.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_tool_initiate(data, input_text, **extra_args)

    def on_tool_complete(self, output: Any, **extra_args: Any) -> dict | Any:
        """
        Runs when a tool process completes. Checks and saves 'geocode_data' in Streamlit state.

        Args:
            output (Any): The tool’s output.

        """
        if isinstance(output, dict) and 'geocode_data' in output:
            geocode_data = {'geocode_data': output['geocode_data'].copy()}
            self.session_state.messages.append(geocode_data)
            output['geocode_data'] = ""
            return output
        return super(CustomCallbackHandler, self).on_tool_complete(output, **extra_args)

    def on_tool_exception(self, error: Union[Exception, KeyboardInterrupt], **extra_args: Any) -> Any:
        """
        Triggered when a tool encounters an error.

        Args:
            error (Union[Exception, KeyboardInterrupt]): The exception or error.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_tool_exception(error, **extra_args)

    def on_generic_text(self, text: str, **extra_args: Any) -> Any:
        """
        Executes on receiving generic text data.

        Args:
            text (str): Text data received.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_generic_text(text, **extra_args)

    def on_agent_event(self, event: AgentEvent, **extra_args: Any) -> Any:
        """
        Triggered on agent-related events.

        Args:
            event (AgentEvent): The agent event data.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_agent_event(event, **extra_args)

    def on_agent_complete(self, result: AgentResult, **extra_args: Any) -> Any:
        """
        Called when an agent process completes.

        Args:
            result (AgentResult): Completion data for the agent.
            **extra_args (Any): Additional parameters.

        """
        return super(CustomCallbackHandler, self).on_agent_complete(result, **extra_args)
