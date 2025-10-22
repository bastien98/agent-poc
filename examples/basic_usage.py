"""Basic usage example of the Strands agent with AWS Bedrock."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from agent_poc.config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent


def main():
    """Basic usage example."""
    # Load environment variables
    load_dotenv()
    settings = get_settings()
    
    # Create Bedrock model
    print("Creating Bedrock model...")
    bedrock_model = create_bedrock_model(settings.aws, settings.bedrock)
    
    # Initialize agent
    print("Initializing agent...")
    agent = StrandsAgent(
        model=bedrock_model,
        config=settings.agent,
        system_prompt="You are a helpful AI assistant. Keep responses concise."
    )
    
    # Example 1: Simple query
    print("\n" + "="*60)
    print("Example 1: Simple Query")
    print("="*60)
    query = "What are the three primary colors?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    # Example 2: Follow-up question (conversation context)
    print("\n" + "="*60)
    print("Example 2: Follow-up Question")
    print("="*60)
    query = "Can you mix them to create other colors?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    # Example 3: Reset and new conversation
    print("\n" + "="*60)
    print("Example 3: Reset Conversation")
    print("="*60)
    agent.reset_conversation()
    query = "What's 2+2?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    print("\n" + "="*60)
    print("Basic usage examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
