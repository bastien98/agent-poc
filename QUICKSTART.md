# Quick Start Guide

Get up and running with the Strands Agent POC in 5 minutes!

## 1. Install Dependencies

```bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

## 2. Configure Your AI Provider

### Option A: OpenAI (Recommended - Easiest Setup)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
```

Edit `.env`:
```bash
AGENT_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o
```

Get your OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)

### Option B: AWS Bedrock (Alternative)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your AWS credentials
# OR configure AWS CLI
aws configure
```

Edit `.env`:
```bash
AGENT_PROVIDER=bedrock
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

#### Get AWS Bedrock Access

1. Log into AWS Console
2. Navigate to Amazon Bedrock
3. Go to "Model access"
4. Request access to Claude 3 models
5. Wait for approval (usually instant)

## 3. Run the Demo

```bash
# Run the main demo
poetry run python -m agent_poc.main
```

Expected output:
```
============================================================
Starting Strands Agent POC
============================================================
Provider: OpenAI
Model: gpt-4o
Agent Name: strands-poc-agent
============================================================
Creating OpenAI model...
Initializing Strands agent...
✓ Agent initialized successfully!

Demo Query: Hello! Please introduce yourself in 2-3 sentences.

Agent Response:
------------------------------------------------------------
[Agent's response will appear here]
------------------------------------------------------------

✓ POC completed successfully!
```

## 4. Try the Examples

### Basic Usage
```bash
poetry run python examples/basic_usage.py
```

### Agent with Tools
```bash
poetry run python examples/agent_with_tools.py
```

### Streaming Responses
```bash
poetry run python examples/streaming_example.py
```

## 5. Use in Your Code

Create a new file `my_agent.py`:

### Using OpenAI
```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.openai_client import create_openai_model
from agent_poc.agent import StrandsAgent

# Setup
load_dotenv()
settings = get_settings()

# Create agent
model = create_openai_model(settings.openai)
agent = StrandsAgent(model=model, config=settings.agent)

# Use agent
response = agent.run("What is machine learning?")
print(response)
```

### Using AWS Bedrock
```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent

# Setup
load_dotenv()
settings = get_settings()

# Create agent
model = create_bedrock_model(settings.aws, settings.bedrock)
agent = StrandsAgent(model=model, config=settings.agent)

# Use agent
response = agent.run("What is machine learning?")
print(response)
```

Run it:
```bash
poetry run python my_agent.py
```

## Common Configuration

### Switch Providers

Edit `.env`:
```bash
# Use OpenAI
AGENT_PROVIDER=openai

# OR use AWS Bedrock
AGENT_PROVIDER=bedrock
```

### Change OpenAI Model

Edit `.env`:
```bash
# Latest GPT-4o (recommended)
OPENAI_MODEL=gpt-4o

# GPT-4 Turbo
OPENAI_MODEL=gpt-4-turbo

# Faster, cheaper
OPENAI_MODEL=gpt-3.5-turbo

# When GPT-5 is released:
OPENAI_MODEL=gpt-5
```

### Change Bedrock Model

Edit `.env`:
```bash
# Faster, cheaper
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0

# More capable
BEDROCK_MODEL_ID=anthropic.claude-3-opus-20240229-v1:0
```

### Adjust Temperature

Edit `.env`:
```bash
# More creative (0-1)
OPENAI_TEMPERATURE=0.9
# or
BEDROCK_TEMPERATURE=0.9

# More focused
OPENAI_TEMPERATURE=0.3
# or
BEDROCK_TEMPERATURE=0.3
```

### Change AWS Region (Bedrock only)

Edit `.env`:
```bash
AWS_REGION=eu-west-1
```

## Adding Tools

```python
from typing import Annotated

def my_tool(query: Annotated[str, "What to search for"]) -> str:
    """Search for something."""
    return f"Results for: {query}"

# Add to agent
agent.add_tool(my_tool)

# Use it
response = agent.run("Search for Python tutorials")
```

## Troubleshooting

### "Module not found"
```bash
poetry install
poetry shell
```

### OpenAI Issues

**"Invalid API key"**
- Check your API key at [platform.openai.com](https://platform.openai.com/api-keys)
- Ensure it's correctly set in `.env`

**"Rate limit exceeded"**
- Check your OpenAI usage limits
- Consider upgrading your plan

### AWS/Bedrock Issues

**"AWS credentials not configured"**
```bash
aws configure
# OR edit .env file
```

**"Access Denied to Bedrock"**
1. Check AWS Console → Bedrock → Model access
2. Request access to the model you're trying to use
3. Wait for approval

**"Region not supported"**
Check [Bedrock regions](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html#bedrock-regions) and update your `.env`

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Check out [examples](examples/README.md) for more use cases
- Read [Strands documentation](https://strandsagents.com/latest/documentation/docs/)
- Explore [OpenAI API docs](https://platform.openai.com/docs)
- Explore [AWS Bedrock docs](https://docs.aws.amazon.com/bedrock/)

## Support

- Create an issue in the repository
- Check OpenAI API status
- Check AWS Bedrock service status
- Review CloudWatch logs for detailed errors (Bedrock)

---

Happy coding! 🚀
