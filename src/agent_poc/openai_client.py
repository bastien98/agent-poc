"""OpenAI model wrapper for Strands Agents."""

import logging
from typing import Any, AsyncIterable, Dict, List, Optional, cast

from openai import OpenAI
from strands.models import Model
from strands.types.content import Message
from strands.types.tools import ToolSpec
from strands.types.streaming import (
    StreamEvent,
    MessageStartEvent,
    MessageStopEvent,
    ContentBlockStartEvent,
    ContentBlockStart,
    ContentBlockStopEvent,
    ContentBlockDeltaEvent,
    ContentBlockDelta,
    ContentBlockDeltaText,
)

from agent_poc.config.settings import OpenAIConfig

logger: logging.Logger = logging.getLogger(__name__)


class OpenAIModel(Model):
    """OpenAI model wrapper that implements the Strands Model interface."""
    
    def __init__(
        self, 
        model: str, 
        api_key: str, 
        temperature: float = 0.7, 
        max_tokens: int = 4096
    ) -> None:
        """Initialize OpenAI model.
        
        Args:
            model: Model name (e.g., "gpt-4o", "gpt-5")
            api_key: OpenAI API key
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        self.model_name: str = model
        self.temperature: float = temperature
        self.max_tokens: int = max_tokens
        self.client: OpenAI = OpenAI(api_key=api_key)
        logger.info(f"Initialized OpenAI model: {model}")
    
    def generate(self, messages: List[Any], **kwargs: Any) -> str:
        """Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional generation parameters
            
        Returns:
            Model response as a string
            
        Raises:
            Exception: If there's an error generating the response
        """
        # Convert Strands message format to OpenAI format if needed
        formatted_messages: List[Dict[str, str]] = self._format_messages(messages)
        
        response: Any = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,  # type: ignore[arg-type]
            temperature=kwargs.get('temperature', self.temperature),
            max_tokens=kwargs.get('max_tokens', self.max_tokens),
            **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens']}
        )
        
        content: Any = response.choices[0].message.content
        return str(content) if content else ""
    
    def _format_messages(self, messages: List[Any]) -> List[Dict[str, str]]:
        """Format messages for OpenAI API.
        
        Args:
            messages: Messages in various formats
            
        Returns:
            List of message dicts for OpenAI
        """
        formatted: List[Dict[str, str]] = []
        for msg in messages:
            if isinstance(msg, dict):
                formatted.append(msg)
            elif hasattr(msg, 'role') and hasattr(msg, 'content'):
                formatted.append({'role': msg.role, 'content': msg.content})
            else:
                formatted.append({'role': 'user', 'content': str(msg)})
        return formatted
    
    # Implement abstract methods from Model base class
    def get_config(self) -> Dict[str, Any]:
        """Get model configuration.
        
        Returns:
            Dictionary of model configuration
        """
        return {
            'model': self.model_name,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
    
    def update_config(self, **kwargs: Any) -> None:
        """Update model configuration.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        if 'temperature' in kwargs:
            self.temperature = float(kwargs['temperature'])
        if 'max_tokens' in kwargs:
            self.max_tokens = int(kwargs['max_tokens'])
    
    async def stream(
        self,
        messages: List[Message],
        tool_specs: Optional[List[ToolSpec]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncIterable[StreamEvent]:
        """Stream responses from the model.
        
        Args:
            messages: List of message objects
            tool_specs: Optional list of tool specifications
            system_prompt: Optional system prompt
            **kwargs: Additional generation parameters
            
        Yields:
            Stream events
        """
        formatted_messages: List[Dict[str, Any]] = self._format_messages_with_system(messages, system_prompt)
        
        # Yield message start event
        yield {'messageStart': MessageStartEvent(role='assistant')}
        
        # Yield content block start event  
        yield {'contentBlockStart': ContentBlockStartEvent(
            start=ContentBlockStart(toolUse=None),
            contentBlockIndex=0
        )}
        
        stream_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,  # type: ignore[arg-type]
            temperature=kwargs.get('temperature', self.temperature),
            max_tokens=kwargs.get('max_tokens', self.max_tokens),
            stream=True,
            **{k: v for k, v in kwargs.items() if k not in ['temperature', 'max_tokens', 'stream']}
        )
        
        for chunk in stream_response:
            if hasattr(chunk, 'choices') and chunk.choices and chunk.choices[0].delta.content:
                # Yield content block delta event with only text
                yield {'contentBlockDelta': ContentBlockDeltaEvent(
                    delta=ContentBlockDelta(
                        text=chunk.choices[0].delta.content
                    ),
                    contentBlockIndex=0
                )}
        
        # Yield content block stop event
        yield {'contentBlockStop': ContentBlockStopEvent(contentBlockIndex=0)}
        
        # Yield message stop event
        yield {'messageStop': MessageStopEvent(
            stopReason='end_turn',
            additionalModelResponseFields=None
        )}
    
    def _format_messages_with_system(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Format messages for OpenAI API including system prompt.
        
        Args:
            messages: Messages in Strands format
            system_prompt: Optional system prompt to prepend
            
        Returns:
            List of message dicts for OpenAI
        """
        formatted: List[Dict[str, Any]] = []
        
        # Add system prompt if provided
        if system_prompt:
            formatted.append({'role': 'system', 'content': system_prompt})
        
        # Format other messages
        for msg in messages:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                # Handle content blocks properly
                if isinstance(msg.content, list):
                    # Check if content blocks have proper structure
                    content_blocks = []
                    for block in msg.content:
                        if hasattr(block, 'text'):
                            # Text content block
                            content_blocks.append({'type': 'text', 'text': block.text})
                        elif isinstance(block, dict):
                            # Already a dict, ensure it has type
                            if 'type' not in block and 'text' in block:
                                block['type'] = 'text'
                            content_blocks.append(block)
                        else:
                            # Convert to text block
                            content_blocks.append({'type': 'text', 'text': str(block)})
                    
                    # If only one text block, simplify to string
                    if len(content_blocks) == 1 and content_blocks[0].get('type') == 'text':
                        formatted.append({'role': msg.role, 'content': content_blocks[0]['text']})
                    else:
                        formatted.append({'role': msg.role, 'content': content_blocks})
                else:
                    # Simple string content
                    formatted.append({'role': msg.role, 'content': str(msg.content)})
            elif isinstance(msg, dict):
                # Already a dict, ensure content format is correct
                if 'content' in msg and isinstance(msg['content'], list):
                    # Ensure each content block has a type
                    content_blocks = []
                    for block in msg['content']:
                        if isinstance(block, dict):
                            if 'type' not in block and 'text' in block:
                                block['type'] = 'text'
                            content_blocks.append(block)
                        else:
                            content_blocks.append({'type': 'text', 'text': str(block)})
                    msg['content'] = content_blocks
                formatted.append(msg)
            else:
                # Fallback
                formatted.append({'role': 'user', 'content': str(msg)})
        
        return formatted
    
    def structured_output(
        self,
        messages: List[Message],
        schema: Dict[str, Any],
        tool_specs: Optional[List[ToolSpec]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate structured output from the model.
        
        Args:
            messages: List of message objects
            schema: JSON schema for the output
            tool_specs: Optional list of tool specifications
            system_prompt: Optional system prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Structured output matching the schema
        """
        # Format messages including system prompt
        formatted_messages = self._format_messages_with_system(messages, system_prompt)
        
        # Placeholder implementation - would need JSON mode or function calling
        response_text = self.generate(messages, **kwargs)
        return {'response': response_text}


def create_openai_model(openai_config: OpenAIConfig) -> OpenAIModel:
    """Create an OpenAI model instance.
    
    Args:
        openai_config: OpenAI-specific configuration
        
    Returns:
        Configured OpenAIModel instance
        
    Raises:
        ValueError: If API key is not configured
    """
    if not openai_config.openai_api_key:
        raise ValueError(
            "OpenAI API key is required. "
            "Please set OPENAI_API_KEY in your .env file or environment variables."
        )
    
    logger.info(f"Creating OpenAI model: {openai_config.openai_model}")
    
    # Create OpenAI model
    model: OpenAIModel = OpenAIModel(
        model=openai_config.openai_model,
        api_key=openai_config.openai_api_key,
        temperature=openai_config.openai_temperature,
        max_tokens=openai_config.openai_max_tokens
    )
    
    return model
