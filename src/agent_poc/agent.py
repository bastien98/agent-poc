"""Strands agent implementation using the official Strands library."""

import logging
from typing import Any, Callable, Generator, List, Optional, Sequence, Union

from strands import Agent
from strands.models import BedrockModel, Model

from agent_poc.config.settings import AgentConfig

logger: logging.Logger = logging.getLogger(__name__)


class StrandsAgent:
    """A wrapper around Strands Agent that supports multiple model providers.
    
    This is a POC implementation that can be extended with tools,
    multi-step reasoning, and more sophisticated agent patterns.
    Supports both AWS Bedrock and OpenAI models.
    """
    
    def __init__(
        self, 
        model: Union[BedrockModel, Model], 
        config: AgentConfig,
        tools: Optional[Sequence[Callable[..., Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> None:
        """Initialize the Strands agent with a model.
        
        Args:
            model: Configured model instance (BedrockModel or custom Model)
            config: Agent configuration
            tools: Optional list of tools for the agent to use
            system_prompt: Optional system prompt to guide agent behavior
        """
        self.config: AgentConfig = config
        self.model: Union[BedrockModel, Model] = model
        
        # Determine model provider
        model_provider: str = "Unknown"
        if isinstance(model, BedrockModel):
            model_provider = "AWS Bedrock"
        elif hasattr(model, 'model_name'):
            model_provider = f"OpenAI ({model.model_name})"
        
        # Default system prompt
        default_system_prompt: str = (
            f"You are a helpful AI assistant powered by {model_provider}. "
            "You provide accurate, thoughtful, and concise responses."
        )
        
        # Initialize Strands Agent
        self.agent: Agent = Agent(
            model=model,
            tools=list(tools) if tools else [],
            system_prompt=system_prompt or default_system_prompt,
            name=config.agent_name
        )
        
        logger.info(f"Initialized {config.agent_name} with Strands Agent framework using {model_provider}")
    
    def run(self, user_input: str, stream: bool = False) -> str:
        """Run the agent with a user input.
        
        Args:
            user_input: User's input/query
            stream: Whether to stream the response
            
        Returns:
            Agent's response as a string
            
        Raises:
            Exception: If there's an error running the agent
        """
        logger.info(f"Processing user input: {user_input[:50]}...")
        
        try:
            # Call the agent directly (uses __call__ method)
            response: Any = self.agent(user_input)
            
            # Extract the final message content from AgentResult
            if hasattr(response, 'message'):
                message: Any = response.message
                if hasattr(message, 'content'):
                    # Content is a list of ContentBlocks
                    content_blocks: Any = message.content
                    if isinstance(content_blocks, list) and len(content_blocks) > 0:
                        # Get text from first content block
                        first_block: Any = content_blocks[0]
                        if hasattr(first_block, 'text'):
                            agent_response: str = first_block.text
                        else:
                            agent_response = str(first_block)
                    else:
                        agent_response = str(content_blocks)
                else:
                    agent_response = str(message)
            else:
                agent_response = str(response)
            
            logger.info("Response generated successfully")
            return agent_response
            
        except Exception as e:
            logger.error(f"Error running agent: {e}", exc_info=True)
            raise
    
    def run_streaming(self, user_input: str) -> Generator[str, None, None]:
        """Run the agent with streaming response.
        
        Args:
            user_input: User's input/query
            
        Yields:
            Chunks of the agent's response
            
        Raises:
            Exception: If there's an error in streaming
        """
        logger.info(f"Processing user input with streaming: {user_input[:50]}...")
        
        try:
            # Use Strands Agent stream_async for streaming
            # Note: For sync usage, we'll need to adapt the async streaming
            response: Any = self.agent(user_input)
            
            # For now, return the full response
            # TODO: Implement proper streaming with stream_async
            if hasattr(response, 'message'):
                message: Any = response.message
                if hasattr(message, 'content'):
                    content_blocks: Any = message.content
                    if isinstance(content_blocks, list) and len(content_blocks) > 0:
                        first_block: Any = content_blocks[0]
                        if hasattr(first_block, 'text'):
                            yield first_block.text
                        else:
                            yield str(first_block)
                    else:
                        yield str(content_blocks)
                else:
                    yield str(message)
            else:
                yield str(response)
                    
        except Exception as e:
            logger.error(f"Error in streaming: {e}", exc_info=True)
            raise
    
    def add_tool(self, tool: Callable[..., Any]) -> None:
        """Add a tool to the agent.
        
        Args:
            tool: A Strands-compatible tool function
        """
        tools_list: List[Any] = getattr(self.agent, 'tools', [])
        tools_list.append(tool)
        logger.info(f"Added tool to agent: {tool}")
    
    def reset_conversation(self) -> None:
        """Reset the agent's conversation history."""
        # Create a new agent instance to reset state
        tools_list: List[Any] = getattr(self.agent, 'tools', [])
        self.agent = Agent(
            model=self.model,
            tools=tools_list,
            system_prompt=self.agent.system_prompt,
            name=self.config.agent_name
        )
        logger.info("Agent conversation reset")
    
    @property
    def conversation_history(self) -> List[Any]:
        """Get the conversation history from the agent.
        
        Returns:
            List of messages in the conversation history
        """
        if hasattr(self.agent, 'messages'):
            return self.agent.messages
        return []
