"""AWS Bedrock model wrapper for Strands Agents."""

import logging
from typing import Any, Dict, Optional

import boto3
from boto3.session import Session

from strands.models import BedrockModel

from agent_poc.config.settings import AWSConfig, BedrockConfig

logger: logging.Logger = logging.getLogger(__name__)


def create_bedrock_model(aws_config: AWSConfig, bedrock_config: BedrockConfig) -> BedrockModel:
    """Create a Strands BedrockModel instance.
    
    Args:
        aws_config: AWS configuration
        bedrock_config: Bedrock-specific configuration
        
    Returns:
        Configured BedrockModel instance
        
    Raises:
        Exception: If there's an error creating the Bedrock model
    """
    # Create boto3 session with credentials if provided
    session_kwargs: Dict[str, Optional[str]] = {
        "region_name": aws_config.aws_region
    }
    
    if aws_config.aws_access_key_id:
        session_kwargs["aws_access_key_id"] = aws_config.aws_access_key_id
    if aws_config.aws_secret_access_key:
        session_kwargs["aws_secret_access_key"] = aws_config.aws_secret_access_key
    if aws_config.aws_session_token:
        session_kwargs["aws_session_token"] = aws_config.aws_session_token
    
    boto_session: Session = boto3.Session(**session_kwargs)  # type: ignore
    
    logger.info(f"Creating BedrockModel with model_id: {bedrock_config.bedrock_model_id}")
    logger.info(f"Region: {aws_config.aws_region}")
    
    # Create Strands BedrockModel
    model: BedrockModel = BedrockModel(
        model_id=bedrock_config.bedrock_model_id,
        boto_session=boto_session,
        temperature=bedrock_config.bedrock_temperature,
        max_tokens=bedrock_config.bedrock_max_tokens
    )
    
    return model
