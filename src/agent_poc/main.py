"""Main entry point for the agent POC."""

import logging
import sys
from typing import NoReturn, Optional, Union

from dotenv import load_dotenv
from strands.models import BedrockModel, Model

from agent_poc.config.settings import get_settings, Settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.openai_client import create_openai_model, OpenAIModel
from agent_poc.agent import StrandsAgent


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def main() -> Optional[StrandsAgent]:
    """Main entry point.
    
    Returns:
        Initialized StrandsAgent instance if successful, None otherwise
        
    Raises:
        SystemExit: If there's an error initializing the agent
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Load configuration
    settings: Settings = get_settings()
    
    # Setup logging
    setup_logging(settings.agent.log_level)
    logger: logging.Logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Strands Agent POC")
    logger.info("=" * 60)
    
    try:
        model: Union[OpenAIModel, BedrockModel]
        system_prompt: str
        
        # Create model based on provider
        if settings.agent.agent_provider == "openai":
            logger.info(f"Provider: OpenAI")
            logger.info(f"Model: {settings.openai.openai_model}")
            logger.info(f"Agent Name: {settings.agent.agent_name}")
            logger.info("=" * 60)
            
            logger.info("Creating OpenAI model...")
            model = create_openai_model(settings.openai)
            
            system_prompt = (
                "You are a helpful AI assistant powered by OpenAI. "
                "You provide accurate, thoughtful, and concise responses."
            )
        else:  # bedrock
            logger.info(f"Provider: AWS Bedrock")
            logger.info(f"AWS Region: {settings.aws.aws_region}")
            logger.info(f"Model: {settings.bedrock.bedrock_model_id}")
            logger.info(f"Agent Name: {settings.agent.agent_name}")
            logger.info("=" * 60)
            
            logger.info("Creating Bedrock model...")
            model = create_bedrock_model(settings.aws, settings.bedrock)
            
            system_prompt = (
                "You are a helpful AI assistant powered by AWS Bedrock. "
                "You provide accurate, thoughtful, and concise responses."
            )
        
        # Initialize Strands agent
        logger.info("Initializing Strands agent...")
        agent: StrandsAgent = StrandsAgent(
            model=model,
            config=settings.agent,
            system_prompt=system_prompt
        )
        
        logger.info("✓ Agent initialized successfully!")
        logger.info("")
        
        # Demo: Simple query
        demo_query: str = "Hello! Please introduce yourself in 2-3 sentences."
        logger.info(f"Demo Query: {demo_query}")
        logger.info("")
        
        response: str = agent.run(demo_query)
        
        logger.info("Agent Response:")
        logger.info("-" * 60)
        logger.info(response)
        logger.info("-" * 60)
        logger.info("")
        logger.info("✓ POC completed successfully!")
        
        return agent
        
    except Exception as e:
        logger.error(f"✗ Error initializing agent: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
