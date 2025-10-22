"""Tests for the Strands agent."""

import pytest
from unittest.mock import Mock, MagicMock

from agent_poc.agent import StrandsAgent
from agent_poc.config.settings import AgentConfig


@pytest.fixture
def mock_bedrock_model():
    """Create a mock Bedrock model."""
    model = Mock()
    return model


@pytest.fixture
def mock_agent_response():
    """Create a mock agent response."""
    response = Mock()
    message = Mock()
    message.content = "Test response from agent"
    response.messages = [message]
    return response


@pytest.fixture
def agent(mock_bedrock_model, monkeypatch):
    """Create an agent instance with mocked dependencies."""
    # Mock the Strands Agent class
    mock_strands_agent = Mock()
    
    def mock_agent_init(model, tools, system_prompt, name):
        return mock_strands_agent
    
    # Import and patch at the module level
    import agent_poc.agent as agent_module
    monkeypatch.setattr(agent_module, "Agent", Mock(return_value=mock_strands_agent))
    
    config = AgentConfig(agent_name="test-agent", log_level="INFO")
    agent_instance = StrandsAgent(mock_bedrock_model, config)
    agent_instance._mock_strands = mock_strands_agent  # Store for test access
    return agent_instance


def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent.config.agent_name == "test-agent"
    assert agent.agent is not None


def test_agent_run(agent, mock_agent_response):
    """Test basic agent run."""
    agent.agent.run = Mock(return_value=mock_agent_response)
    
    response = agent.run("Hello")
    
    assert response == "Test response from agent"
    agent.agent.run.assert_called_once_with("Hello", stream=False)


def test_agent_add_tool(agent):
    """Test adding a tool to the agent."""
    mock_tool = Mock()
    agent.agent.tools = []
    
    agent.add_tool(mock_tool)
    
    assert mock_tool in agent.agent.tools


def test_agent_reset_conversation(agent, mock_bedrock_model, monkeypatch):
    """Test conversation reset."""
    # Mock Agent class for reset
    import agent_poc.agent as agent_module
    mock_new_agent = Mock()
    monkeypatch.setattr(agent_module, "Agent", Mock(return_value=mock_new_agent))
    
    agent.reset_conversation()
    
    # Verify a new agent was created
    assert agent.agent == mock_new_agent


def test_conversation_history_property(agent):
    """Test conversation history property."""
    mock_messages = [Mock(), Mock()]
    agent.agent.messages = mock_messages
    
    history = agent.conversation_history
    
    assert history == mock_messages


def test_conversation_history_empty(agent):
    """Test conversation history when no messages exist."""
    # Remove messages attribute
    if hasattr(agent.agent, 'messages'):
        delattr(agent.agent, 'messages')
    
    history = agent.conversation_history
    
    assert history == []
