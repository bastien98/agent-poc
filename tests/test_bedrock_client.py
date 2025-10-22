"""Tests for the Bedrock model creation."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.config.settings import AWSConfig, BedrockConfig


@pytest.fixture
def aws_config():
    """Create test AWS configuration."""
    return AWSConfig(
        aws_region="us-east-1",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret"
    )


@pytest.fixture
def bedrock_config():
    """Create test Bedrock configuration."""
    return BedrockConfig(
        bedrock_model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        bedrock_max_tokens=1000,
        bedrock_temperature=0.5
    )


@patch("agent_poc.bedrock_client.boto3")
@patch("agent_poc.bedrock_client.BedrockModel")
def test_create_bedrock_model(mock_bedrock_model_class, mock_boto3, aws_config, bedrock_config):
    """Test Bedrock model creation."""
    mock_session = Mock()
    mock_boto3.Session.return_value = mock_session
    
    mock_model_instance = Mock()
    mock_bedrock_model_class.return_value = mock_model_instance
    
    result = create_bedrock_model(aws_config, bedrock_config)
    
    # Verify boto3 session was created with correct parameters
    mock_boto3.Session.assert_called_once_with(
        region_name="us-east-1",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret"
    )
    
    # Verify BedrockModel was instantiated correctly
    mock_bedrock_model_class.assert_called_once_with(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        boto_session=mock_session,
        temperature=0.5,
        max_tokens=1000
    )
    
    assert result == mock_model_instance


@patch("agent_poc.bedrock_client.boto3")
@patch("agent_poc.bedrock_client.BedrockModel")
def test_create_bedrock_model_without_credentials(
    mock_bedrock_model_class, mock_boto3, bedrock_config
):
    """Test Bedrock model creation without explicit credentials."""
    aws_config = AWSConfig(aws_region="us-west-2")
    
    mock_session = Mock()
    mock_boto3.Session.return_value = mock_session
    
    mock_model_instance = Mock()
    mock_bedrock_model_class.return_value = mock_model_instance
    
    result = create_bedrock_model(aws_config, bedrock_config)
    
    # Verify session created with only region
    mock_boto3.Session.assert_called_once_with(region_name="us-west-2")
    
    assert result == mock_model_instance


@patch("agent_poc.bedrock_client.boto3")
@patch("agent_poc.bedrock_client.BedrockModel")
def test_create_bedrock_model_with_session_token(
    mock_bedrock_model_class, mock_boto3, bedrock_config
):
    """Test Bedrock model creation with session token."""
    aws_config = AWSConfig(
        aws_region="eu-west-1",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret",
        aws_session_token="test-token"
    )
    
    mock_session = Mock()
    mock_boto3.Session.return_value = mock_session
    
    mock_model_instance = Mock()
    mock_bedrock_model_class.return_value = mock_model_instance
    
    result = create_bedrock_model(aws_config, bedrock_config)
    
    # Verify session created with all credentials including token
    mock_boto3.Session.assert_called_once_with(
        region_name="eu-west-1",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret",
        aws_session_token="test-token"
    )
    
    assert result == mock_model_instance
