"""Application settings using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSConfig(BaseSettings):
    """AWS configuration settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_session_token: str | None = None


class BedrockConfig(BaseSettings):
    """AWS Bedrock configuration settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    bedrock_max_tokens: int = 4096
    bedrock_temperature: float = 0.7


class BedrockKnowledgeBaseConfig(BaseSettings):
    """AWS Bedrock Knowledge Base configuration settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    bedrock_kb_id: str | None = None
    bedrock_kb_region: str = "us-east-1"


class OpenAIConfig(BaseSettings):
    """OpenAI configuration settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o"  # Latest GPT-4 model, can be changed to gpt-5 when available
    openai_max_tokens: int = 4096
    openai_temperature: float = 0.7


class AgentConfig(BaseSettings):
    """Agent configuration settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    agent_name: str = "strands-poc-agent"
    agent_provider: str = "openai"  # Can be "openai" or "bedrock"
    log_level: str = "INFO"


class Settings(BaseSettings):
    """Main application settings."""
    
    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")
    
    aws: AWSConfig = AWSConfig()
    bedrock: BedrockConfig = BedrockConfig()
    bedrock_kb: BedrockKnowledgeBaseConfig = BedrockKnowledgeBaseConfig()
    openai: OpenAIConfig = OpenAIConfig()
    agent: AgentConfig = AgentConfig()


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
