"""Test the Bedrock Knowledge Base tool directly without the agent."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from agent_poc.config.settings import get_settings
from agent_poc.tools import query_bedrock_knowledge_base


def main():
    """Test the KB query tool directly."""
    # Load environment variables
    load_dotenv()
    settings = get_settings()
    
    print("="*60)
    print("Bedrock Knowledge Base Tool Test")
    print("="*60)
    
    # Check configuration
    if not settings.bedrock_kb.bedrock_kb_id:
        print("❌ Error: BEDROCK_KB_ID is not configured")
        print()
        print("Please set BEDROCK_KB_ID in your .env file:")
        print("Example: BEDROCK_KB_ID=ABCD1234EFGH")
        print()
        print("You can find your Knowledge Base ID in the AWS Console:")
        print("1. Go to Amazon Bedrock > Knowledge bases")
        print("2. Select your knowledge base")
        print("3. Copy the Knowledge base ID")
        return
    
    print(f"✓ Knowledge Base ID: {settings.bedrock_kb.bedrock_kb_id}")
    print(f"✓ Region: {settings.bedrock_kb.bedrock_kb_region}")
    print()
    
    # Check AWS credentials
    if not settings.aws.aws_access_key_id:
        print("⚠️  Warning: AWS credentials not found in .env")
        print("   Will attempt to use default AWS credentials from environment/profile")
        print()
    else:
        print(f"✓ AWS Access Key ID: {settings.aws.aws_access_key_id[:10]}...")
        print()
    
    # Test query
    test_query = input("Enter a test query (or press Enter for default): ").strip()
    if not test_query:
        test_query = "What information is available?"
    
    print()
    print(f"Querying knowledge base with: '{test_query}'")
    print("="*60)
    print()
    
    try:
        result = query_bedrock_knowledge_base(test_query, max_results=3)
        print(result)
        print()
        print("="*60)
        print("✓ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Common issues:")
        print("1. Check if your AWS credentials are correct")
        print("2. Verify the Knowledge Base ID exists")
        print("3. Ensure your AWS credentials have bedrock:Retrieve permissions")
        print("4. Check if the Knowledge Base is in the correct region")


if __name__ == "__main__":
    main()
