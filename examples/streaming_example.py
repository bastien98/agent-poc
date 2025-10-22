"""Example of streaming responses from the Strands agent."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from agent_poc.config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent


def main():
    """Streaming response example."""
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
        system_prompt="You are a creative storyteller."
    )
    
    # Example: Streaming a story
    print("\n" + "="*60)
    print("Streaming Example: Generate a Short Story")
    print("="*60)
    query = "Tell me a very short story about a robot learning to paint."
    print(f"Query: {query}\n")
    print("Response (streaming):")
    print("-" * 60)
    
    try:
        for chunk in agent.run_streaming(query):
            print(chunk, end="", flush=True)
    except Exception as e:
        print(f"\nNote: Streaming may not be fully supported depending on the model.")
        print(f"Error: {e}")
        print("\nFalling back to regular response:")
        print(agent.run(query))
    
    print("\n" + "-" * 60)
    print("\n" + "="*60)
    print("Streaming example completed!")
    print("="*60)


if __name__ == "__main__":
    main()
