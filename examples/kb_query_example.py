"""Example of using the Bedrock Knowledge Base query tool with the agent."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from agent_poc.config.settings import get_settings
from agent_poc.openai_client import create_openai_model
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent
from agent_poc.tools import query_bedrock_knowledge_base, get_current_time


def main():
    """Example of agent querying a Bedrock Knowledge Base."""
    # Load environment variables
    load_dotenv()
    settings = get_settings()
    
    # Check if KB is configured
    if not settings.bedrock_kb.bedrock_kb_id:
        print("⚠️  Warning: BEDROCK_KB_ID is not configured in .env file")
        print("Please set BEDROCK_KB_ID to your Bedrock Knowledge Base ID")
        print("Example: BEDROCK_KB_ID=ABCD1234EFGH")
        return
    
    print("="*60)
    print("Bedrock Knowledge Base Query Example")
    print("="*60)
    print(f"Knowledge Base ID: {settings.bedrock_kb.bedrock_kb_id}")
    print(f"Region: {settings.bedrock_kb.bedrock_kb_region}")
    print(f"Provider: {settings.agent.agent_provider}")
    print("="*60)
    print()
    
    # Create model based on provider
    if settings.agent.agent_provider == "openai":
        print("Creating OpenAI model...")
        model = create_openai_model(settings.openai)
    else:
        print("Creating Bedrock model...")
        model = create_bedrock_model(settings.aws, settings.bedrock)
    
    # Initialize agent with KB query tool
    print("Initializing agent with Knowledge Base query tool...")
    agent = StrandsAgent(
        model=model,
        config=settings.agent,
        tools=[query_bedrock_knowledge_base, get_current_time],
        system_prompt=(
            "You are a helpful AI assistant with access to a knowledge base. "
            "When users ask questions, use the query_bedrock_knowledge_base tool to search for relevant information. "
            "Always cite the sources when providing information from the knowledge base. "
            "Be concise but thorough in your responses."
        )
    )
    
    print("✓ Agent initialized successfully!")
    print()
    
    # Example queries
    queries = [
        "What information do you have about product features?",
        "Can you find documentation about API endpoints?",
        "Search for information about pricing plans"
    ]
    
    for i, query in enumerate(queries, 1):
        print("\n" + "="*60)
        print(f"Example {i}: Knowledge Base Query")
        print("="*60)
        print(f"Query: {query}")
        print()
        print("Agent Response:")
        print("-"*60)
        
        try:
            response = agent.run(query)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
        
        print("-"*60)
        
        # Only run first query if in demo mode
        if i == 1:
            print()
            print("💡 Tip: Modify the queries list to test with your actual knowledge base content")
            break
    
    print()
    print("="*60)
    print("Knowledge Base query examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
