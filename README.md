# agent-poc


A proof of concept project for developing a Strands-based agent that supports multiple AI providers (OpenAI GPT and AWS Bedrock) using the official [Strands Agents](https://strandsagents.com) library.

## Overview

This project demonstrates how to build an AI agent using:
- **Strands Agents**: Official framework for building conversational AI agents
- **OpenAI**: GPT-4o, GPT-4 Turbo, and future GPT-5 support
- **AWS Bedrock**: Managed service for foundation models (Claude 3)
- **Poetry**: Modern Python dependency management
- **Pydantic**: Configuration and data validation

## Project Structure

```
agent-poc/
├── src/
│   └── agent_poc/
│       ├── __init__.py
│       ├── main.py            # Entry point
│       ├── agent.py           # Strands agent wrapper
│       ├── openai_client.py   # OpenAI model configuration
│       ├── bedrock_client.py  # AWS Bedrock model configuration
│       ├── tools.py           # Custom tools for the agent
│       └── config/
│           ├── __init__.py
│           └── settings.py    # Configuration management
├── tests/                     # Unit tests
├── examples/                  # Usage examples
├── .env.example              # Environment variables template
├── pyproject.toml            # Project dependencies
└── README.md
```

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- **For OpenAI**: OpenAI API key
- **For AWS Bedrock**: AWS Account with Bedrock access and AWS credentials configured

## Installation

1. **Install Poetry** (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Clone and setup the project**:
```bash
git clone <repository-url>
cd agent-poc
poetry install
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

## Configuration

The agent supports two AI providers: **OpenAI** (recommended) and **AWS Bedrock**.

### OpenAI Configuration (Default - Recommended)

Edit the `.env` file:
```bash
# Set provider to OpenAI
AGENT_PROVIDER=openai

# Add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Choose your model (gpt-4o is recommended, gpt-5 when available)
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.7
```

**Available OpenAI Models:**
- `gpt-4o` (default - most capable, multimodal)
- `gpt-4-turbo` (fast and capable)
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-5` (use when available - update as soon as released!)

To get an OpenAI API key:
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key

### AWS Bedrock Configuration (Alternative)

If you prefer to use AWS Bedrock with Claude models, edit the `.env` file:

```bash
# Set provider to Bedrock
AGENT_PROVIDER=bedrock

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Bedrock Model
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_MAX_TOKENS=4096
BEDROCK_TEMPERATURE=0.7
```

#### Setting up AWS Credentials

You have several options to configure AWS credentials:

**Option 1: Environment Variables (Development)**
Edit the `.env` file with your AWS credentials

**Option 2: AWS CLI Configuration (Recommended for Development)**
```bash
aws configure
```

**Option 3: IAM Role (Recommended for Production)**
When deploying to AWS (EC2, ECS, Lambda), use IAM roles instead of hardcoded credentials.

#### Bedrock Model Access

1. Go to AWS Console → Bedrock → Model access
2. Request access to Claude 3 models
3. Wait for approval (usually instant for most models)
4. Update `BEDROCK_MODEL_ID` in `.env` if using a different model

**Available Bedrock Models:**
- `anthropic.claude-3-sonnet-20240229-v1:0` (default - balanced)
- `anthropic.claude-3-haiku-20240307-v1:0` (faster, cheaper)
- `anthropic.claude-3-opus-20240229-v1:0` (most capable)

## Usage

### Running the Agent

```bash
poetry run python -m agent_poc.main
```

Or using the installed script:
```bash
poetry run agent-poc
```

### Basic Usage in Your Code

#### Using OpenAI (Recommended)

```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.openai_client import create_openai_model
from agent_poc.agent import StrandsAgent

# Load configuration
load_dotenv()
settings = get_settings()

# Create OpenAI model
model = create_openai_model(settings.openai)

# Initialize agent
agent = StrandsAgent(
    model=model,
    config=settings.agent,
    system_prompt="You are a helpful AI assistant."
)

# Run agent
response = agent.run("What is the capital of France?")
print(response)
```

#### Using AWS Bedrock (Alternative)

```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent

# Load configuration
load_dotenv()
settings = get_settings()

# Create Bedrock model
model = create_bedrock_model(settings.aws, settings.bedrock)

# Initialize agent
agent = StrandsAgent(
    model=model,
    config=settings.agent,
    system_prompt="You are a helpful AI assistant."
)

# Run agent
response = agent.run("What is the capital of France?")
print(response)
```

### Using with Tools

```python
from agent_poc.tools import get_current_time, calculate

# Initialize agent with tools
agent = StrandsAgent(
    model=model,
    config=settings.agent,
    tools=[get_current_time, calculate]
)

# Agent can now use tools
response = agent.run("What time is it? Also, what is 25 * 4?")
print(response)
```

### Streaming Responses

```python
# Run with streaming
for chunk in agent.run_streaming("Tell me a short story"):
    print(chunk, end="", flush=True)
```

## Understanding Strands Agents

Strands Agents is a powerful framework that provides:

- **Agent Loop**: Automatic reasoning and tool use loop
- **Tool Integration**: Easy integration of custom tools and functions
- **Model Providers**: Support for multiple LLM providers (Bedrock, OpenAI, etc.)
- **Conversation Management**: Built-in conversation history and context management

### Key Concepts

1. **Agent**: The main orchestrator that manages the conversation and tool use
2. **Model**: The underlying LLM (in our case, AWS Bedrock)
3. **Tools**: Functions the agent can call to perform actions or retrieve information
4. **System Prompt**: Instructions that guide the agent's behavior

Learn more at [strandsagents.com](https://strandsagents.com/latest/documentation/docs/)

## Development

### Running Tests

```bash
poetry run pytest
poetry run pytest --cov=agent_poc  # With coverage
poetry run pytest -v  # Verbose output
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/

# Lint code
poetry run ruff check src/ tests/
```

### Adding Dependencies

```bash
poetry add package-name
poetry add --group dev package-name  # Development dependency
```

## Configuration

All configuration is managed through environment variables and the `config/settings.py` module.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |
| `BEDROCK_MODEL_ID` | `anthropic.claude-3-sonnet-...` | Bedrock model to use |
| `BEDROCK_MAX_TOKENS` | `4096` | Maximum tokens in response |
| `BEDROCK_TEMPERATURE` | `0.7` | Model temperature (0-1) |
| `AGENT_NAME` | `strands-poc-agent` | Agent identifier |
| `LOG_LEVEL` | `INFO` | Logging level |

## Creating Custom Tools

Tools are functions that the agent can call. Here's how to create one:

```python
from typing import Annotated

def my_custom_tool(
    param: Annotated[str, "Description of parameter"]
) -> str:
    """Tool description that the agent will see.
    
    Args:
        param: Parameter description
        
    Returns:
        Result description
    """
    # Your tool logic here
    return f"Result for {param}"

# Add to agent
agent.add_tool(my_custom_tool)
```

The agent will automatically:
- Understand what the tool does from the docstring
- Know when to use it based on user queries
- Parse parameters correctly
- Handle the tool's response

## Production Deployment

### Considerations for Production

1. **Use IAM Roles**: Never hardcode credentials in production
2. **Secret Management**: Use AWS Secrets Manager or Parameter Store
3. **Monitoring**: Add CloudWatch metrics and logs
4. **Error Handling**: Implement retry logic and circuit breakers
5. **Rate Limiting**: Implement request throttling
6. **Cost Management**: Monitor token usage and implement budgets
7. **Tool Safety**: Validate and sanitize tool inputs/outputs

### Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/
COPY config/ ./config/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Set environment
ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "agent-poc"]
```

### AWS Lambda Deployment

For Lambda deployment, consider:
- Using Lambda Layers for dependencies
- Optimizing cold start times
- Managing memory allocation (model operations are memory-intensive)
- Using provisioned concurrency for production workloads

## Extending the POC

### Adding RAG (Retrieval Augmented Generation)

```python
from agent_poc.tools import search_knowledge_base

# Implement actual vector database search
def enhanced_search(query: str) -> str:
    # Connect to your vector DB (Pinecone, Weaviate, etc.)
    # Perform similarity search
    # Return relevant context
    pass

agent.add_tool(enhanced_search)
```

### Multi-Agent Systems

Create multiple specialized agents:

```python
# Research agent
research_agent = StrandsBedrockAgent(
    model=bedrock_model,
    config=settings.agent,
    system_prompt="You are a research specialist..."
)

# Writing agent
writing_agent = StrandsBedrockAgent(
    model=bedrock_model,
    config=settings.agent,
    system_prompt="You are a technical writer..."
)
```

### Adding Memory

Integrate external memory systems:

```python
# Add conversation persistence
import json

def save_conversation(agent):
    history = agent.conversation_history
    with open("memory.json", "w") as f:
        json.dump(history, f)

def load_conversation(agent):
    with open("memory.json", "r") as f:
        history = json.load(f)
    # Restore to agent
```

## Troubleshooting

### Common Issues

1. **"Could not connect to Bedrock"**
   - Check AWS credentials
   - Verify region supports Bedrock
   - Ensure model access is granted

2. **"Rate limit exceeded"**
   - Implement exponential backoff
   - Check service quotas in AWS Console

3. **"Invalid model ID"**
   - Verify model ID in Bedrock console
   - Check model availability in your region

4. **"Module 'strands' not found"**
   - Run `poetry install` to install dependencies
   - Verify you're in the poetry shell: `poetry shell`

5. **Agent not using tools**
   - Check tool docstrings are clear and descriptive
   - Ensure type hints with Annotated descriptions
   - Verify tools are added to agent before run

## Resources

- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/docs/)
- [Strands Agents API Reference](https://strandsagents.com/latest/documentation/docs/api-reference/agent/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Poetry Documentation](https://python-poetry.org/docs/)

## License

MIT

## Author

Bastien Moenaert (bastien.moenaert@persgroep.net)
