"""Example of using the Strands agent with custom tools."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from agent_poc.config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent
from agent_poc.tools import get_current_time, calculate, search_knowledge_base


def main():
    """Example of agent with tools."""
    # Load environment variables
    load_dotenv()
    settings = get_settings()
    
    # Create Bedrock model
    print("Creating Bedrock model...")
    bedrock_model = create_bedrock_model(settings.aws, settings.bedrock)
    
    # Initialize agent with tools
    print("Initializing agent with tools...")
    agent = StrandsAgent(
        model=bedrock_model,
        config=settings.agent,
        tools=[get_current_time, calculate, search_knowledge_base],
        system_prompt=(
            "You are a helpful AI assistant with access to tools. "
            "Use the tools when appropriate to provide accurate information. "
            "When using tools, explain what you're doing."
        )
    )
    
    # Example 1: Using time tool
    print("\n" + "="*60)
    print("Example 1: Using Time Tool")
    print("="*60)
    query = "What time is it right now?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    # Example 2: Using calculator tool
    print("\n" + "="*60)
    print("Example 2: Using Calculator Tool")
    print("="*60)
    query = "Can you calculate 15 * 23 + 47 for me?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    # Example 3: Using search tool
    print("\n" + "="*60)
    print("Example 3: Using Search Tool")
    print("="*60)
    query = "Search for information about Python programming"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    # Example 4: Complex query using multiple tools
    print("\n" + "="*60)
    print("Example 4: Multiple Tools")
    print("="*60)
    query = "What time is it, and what is 100 divided by 4?"
    print(f"Query: {query}")
    print(f"Response: {agent.run(query)}")
    
    print("\n" + "="*60)
    print("Tool usage examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
