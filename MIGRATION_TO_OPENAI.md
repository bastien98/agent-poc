# Migration to OpenAI (GPT-4o / GPT-5 Ready)

## Summary of Changes

Your agent has been successfully upgraded to support **OpenAI's GPT models** (including GPT-4o, GPT-4 Turbo, and will support GPT-5 when released) while maintaining backward compatibility with AWS Bedrock.

## What Changed

### 1. New Dependencies
- Added `openai` package (version 2.6.0) for OpenAI API integration

### 2. New Files Created
- `src/agent_poc/openai_client.py` - OpenAI model wrapper for Strands Agents

### 3. Updated Files

#### `config/settings.py`
- Added `OpenAIConfig` class for OpenAI configuration
- Added `agent_provider` setting to switch between "openai" and "bedrock"
- OpenAI settings include: API key, model selection, temperature, max tokens

#### `src/agent_poc/agent.py`
- Renamed `StrandsBedrockAgent` to `StrandsAgent` (more generic)
- Now supports both `BedrockModel` and `OpenAIModel`
- Automatically detects provider and adjusts system prompts

#### `src/agent_poc/main.py`
- Added logic to select provider based on configuration
- Creates appropriate model (OpenAI or Bedrock) based on `AGENT_PROVIDER` setting
- Shows provider-specific information on startup

#### `.env.example`
- Added OpenAI configuration variables
- Added `AGENT_PROVIDER` to switch between providers
- Updated with comments for GPT-5 readiness

#### Documentation
- Updated `README.md` with OpenAI setup instructions
- Updated `QUICKSTART.md` with OpenAI as the recommended option
- Both maintain full AWS Bedrock documentation

## How to Use

### Quick Start with OpenAI (Recommended)

1. **Get an OpenAI API Key**
   - Go to [platform.openai.com](https://platform.openai.com/api-keys)
   - Sign up or log in
   - Create a new API key

2. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

3. **Configure for OpenAI**
   Edit `.env`:
   ```bash
   AGENT_PROVIDER=openai
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4o
   OPENAI_MAX_TOKENS=4096
   OPENAI_TEMPERATURE=0.7
   ```

4. **Run the agent**
   ```bash
   poetry run python -m agent_poc.main
   ```

### Switching to GPT-5 (When Available)

Simply update your `.env` file:
```bash
OPENAI_MODEL=gpt-5
```

No code changes required!

### Available OpenAI Models

- `gpt-4o` - Latest GPT-4 Omni (recommended)
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - Faster, cheaper option
- `gpt-5` - Ready for when OpenAI releases it

### Continue Using AWS Bedrock

Your existing AWS Bedrock setup still works! Just set:
```bash
AGENT_PROVIDER=bedrock
```

All your existing AWS credentials and configuration remain unchanged.

## Code Examples

### Using OpenAI in Your Code

```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.openai_client import create_openai_model
from agent_poc.agent import StrandsAgent

load_dotenv()
settings = get_settings()

# Create OpenAI model
model = create_openai_model(settings.openai)

# Create agent
agent = StrandsAgent(
    model=model,
    config=settings.agent,
    system_prompt="You are a helpful assistant."
)

# Use the agent
response = agent.run("Explain quantum computing in simple terms")
print(response)
```

### Provider-Agnostic Code

```python
from dotenv import load_dotenv
from agent_poc.config.settings import get_settings
from agent_poc.openai_client import create_openai_model
from agent_poc.bedrock_client import create_bedrock_model
from agent_poc.agent import StrandsAgent

load_dotenv()
settings = get_settings()

# Automatically select provider based on config
if settings.agent.agent_provider == "openai":
    model = create_openai_model(settings.openai)
else:
    model = create_bedrock_model(settings.aws, settings.bedrock)

# Same agent code works with both providers
agent = StrandsAgent(model=model, config=settings.agent)
response = agent.run("Your query here")
```

## Benefits of This Upgrade

1. **Access to Latest GPT Models**: Use GPT-4o and be ready for GPT-5
2. **Easier Setup**: OpenAI is simpler than AWS Bedrock for most users
3. **Cost Flexibility**: Choose between OpenAI and AWS based on your needs
4. **Future-Proof**: Ready for GPT-5 without code changes
5. **Backward Compatible**: Existing Bedrock setup continues to work

## Troubleshooting

### OpenAI API Key Issues
```bash
# Check your API key is set correctly
echo $OPENAI_API_KEY  # (after loading .env)

# Make sure it starts with 'sk-'
# Get a new key at: https://platform.openai.com/api-keys
```

### Rate Limits
OpenAI has different rate limits based on your account tier. If you hit limits:
- Check your usage at [platform.openai.com/usage](https://platform.openai.com/usage)
- Consider upgrading your OpenAI plan
- Or switch to AWS Bedrock: `AGENT_PROVIDER=bedrock`

### Module Import Errors
```bash
# Reinstall dependencies
poetry install

# Or update the lock file
poetry lock
poetry install
```

## Cost Comparison

### OpenAI GPT-4o (as of 2025)
- Input: ~$2.50 per 1M tokens
- Output: ~$10 per 1M tokens
- Fast and capable

### AWS Bedrock Claude 3 Sonnet
- Input: ~$3.00 per 1M tokens
- Output: ~$15 per 1M tokens
- Requires AWS setup

*Prices may vary - check current pricing with providers*

## Next Steps

1. Create your `.env` file with OpenAI credentials
2. Run the demo: `poetry run python -m agent_poc.main`
3. Test with your own queries
4. When GPT-5 launches, simply update `OPENAI_MODEL=gpt-5`

## Support

- OpenAI Documentation: [platform.openai.com/docs](https://platform.openai.com/docs)
- Strands Agents: [strandsagents.com](https://strandsagents.com)
- Issues: Create an issue in this repository

---

**Note**: GPT-5 is not yet released by OpenAI. When it becomes available, you can immediately use it by updating the `OPENAI_MODEL` environment variable. The codebase is ready!
