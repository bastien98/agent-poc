"""Tests for configuration settings."""

import pytest
from agent_poc.config.settings import AWSConfig, BedrockConfig, AgentConfig, Settings, get_settings


def test_aws_config_defaults():
    """Test AWS config default values."""
    config = AWSConfig()
    assert config.aws_region == "us-east-1"
    assert config.aws_access_key_id is None


def test_bedrock_config_defaults():
    """Test Bedrock config default values."""
    config = BedrockConfig()
    assert config.bedrock_model_id == "anthropic.claude-3-sonnet-20240229-v1:0"
    assert config.bedrock_max_tokens == 4096
    assert config.bedrock_temperature == 0.7


def test_agent_config_defaults():
    """Test Agent config default values."""
    config = AgentConfig()
    assert config.agent_name == "strands-poc-agent"
    assert config.log_level == "INFO"


def test_settings_initialization():
    """Test main settings initialization."""
    settings = Settings()
    assert isinstance(settings.aws, AWSConfig)
    assert isinstance(settings.bedrock, BedrockConfig)
    assert isinstance(settings.agent, AgentConfig)


def test_get_settings():
    """Test get_settings factory function."""
    settings = get_settings()
    assert isinstance(settings, Settings)
