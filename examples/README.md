# Examples

This directory contains example scripts demonstrating various features of the Strands agent POC.

## Prerequisites

Before running examples, make sure you have:
1. Installed dependencies: `poetry install`
2. Configured your `.env` file with AWS credentials
3. Granted access to Bedrock models in AWS Console

## Running Examples

### Basic Usage

Demonstrates simple queries and conversation management:

```bash
poetry run python examples/basic_usage.py
```

### Agent with Tools

Shows how to use the agent with custom tools:

```bash
poetry run python examples/agent_with_tools.py
```

### Streaming Responses

Demonstrates streaming responses from the agent:

```bash
poetry run python examples/streaming_example.py
```

## What Each Example Shows

### basic_usage.py
- Creating a Bedrock model
- Initializing a Strands agent
- Making simple queries
- Conversation context
- Resetting conversations

### agent_with_tools.py
- Adding tools to the agent
- Tool usage (time, calculator, search)
- Multiple tool usage in one query
- How agents decide when to use tools

### streaming_example.py
- Streaming responses for better UX
- Real-time output display
- Handling streaming vs non-streaming responses

## Creating Your Own Examples

Feel free to create your own example scripts! Just:

1. Import the necessary modules
2. Load settings from `.env`
3. Create your agent configuration
4. Experiment with different prompts and tools

Example template:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsBedrockAgent

def main():
    load_dotenv()
    settings = get_settings()
    
    bedrock_model = create_bedrock_model(settings.aws, settings.bedrock)
    agent = StrandsBedrockAgent(model=bedrock_model, config=settings.agent)
    
    # Your code here
    response = agent.run("Your query here")
    print(response)

if __name__ == "__main__":
    main()
```

## Troubleshooting

If examples fail to run:

1. **Import errors**: Make sure you're running from the project root with `poetry run`
2. **AWS errors**: Check your `.env` configuration and AWS credentials
3. **Model access errors**: Verify Bedrock model access in AWS Console
4. **Rate limits**: Add delays between requests if hitting rate limits
