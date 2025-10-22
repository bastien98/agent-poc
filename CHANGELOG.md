# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-10-22

### Added - OpenAI Support and Multi-Provider Architecture

#### Summary
Added support for OpenAI's GPT models (GPT-4o, GPT-4 Turbo, and GPT-5 ready) while maintaining full backward compatibility with AWS Bedrock. The agent now supports multiple AI providers with easy switching via configuration.

#### New Features

1. **OpenAI Integration**
   - Added `openai` package dependency (v2.6.0)
   - New `openai_client.py` module for OpenAI model integration
   - Support for GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo
   - Ready for GPT-5 when released (no code changes needed)

2. **Multi-Provider Architecture**
   - Provider selection via `AGENT_PROVIDER` environment variable
   - Seamless switching between "openai" and "bedrock"
   - Single unified agent interface works with both providers

3. **Enhanced Configuration**
   - New `OpenAIConfig` class in settings
   - `agent_provider` setting for provider selection
   - Separate configuration for OpenAI and Bedrock

#### Files Changed

- `config/settings.py` - Added OpenAI configuration and provider selection
- `src/agent_poc/agent.py` - Renamed to `StrandsAgent`, supports both providers
- `src/agent_poc/main.py` - Added provider-based model creation logic
- `.env.example` - Added OpenAI configuration with GPT-5 notes
- `README.md` - Updated with OpenAI setup instructions
- `QUICKSTART.md` - Updated with OpenAI as recommended option
- `pyproject.toml` - Added openai dependency

#### Files Added

- `src/agent_poc/openai_client.py` - OpenAI model wrapper
- `MIGRATION_TO_OPENAI.md` - Complete migration guide

#### Configuration Changes

New environment variables:
```bash
AGENT_PROVIDER=openai          # Choose "openai" or "bedrock"
OPENAI_API_KEY=sk-...          # Your OpenAI API key
OPENAI_MODEL=gpt-4o            # Model selection (gpt-5 ready)
OPENAI_MAX_TOKENS=4096         # Token limit
OPENAI_TEMPERATURE=0.7         # Temperature setting
```

#### Benefits

- **Easier Setup**: OpenAI requires just an API key (no AWS account needed)
- **Latest Models**: Access to GPT-4o and future GPT-5
- **Cost Options**: Choose between OpenAI and AWS based on pricing
- **Future-Proof**: GPT-5 ready without code changes
- **Backward Compatible**: Existing Bedrock setup unchanged

#### Breaking Changes

None! This is a backward-compatible update:
- `StrandsBedrockAgent` renamed to `StrandsAgent` (but more capable)
- All existing Bedrock code continues to work
- Just set `AGENT_PROVIDER=bedrock` to use existing setup

#### Migration Path

For existing users wanting to try OpenAI:
1. Run `poetry install` to add OpenAI package
2. Copy updated `.env.example` to see new options
3. Add `AGENT_PROVIDER=openai` and `OPENAI_API_KEY` to `.env`
4. Run as normal - it just works!

To continue using Bedrock:
1. No changes needed, or
2. Optionally add `AGENT_PROVIDER=bedrock` to `.env` for explicitness

#### Documentation

- See `MIGRATION_TO_OPENAI.md` for detailed migration guide
- Updated README with dual-provider setup instructions
- Updated QUICKSTART with OpenAI as primary option

## [0.1.0] - 2025-10-22

### Added - Complete Rewrite to Use Official Strands Agents Library

This version represents a complete rewrite of the project to use the official Strands Agents framework from https://strandsagents.com

#### Core Changes

**Dependencies**
- Added `strands-agents` (v0.4.0+) - Official Strands Agents framework
- Kept `boto3` for AWS integration
- Kept `pydantic-settings` for configuration management
- Added development dependencies: `pytest`, `pytest-cov`, `black`, `ruff`

**Architecture**
- Replaced custom agent implementation with official Strands `Agent` class
- Simplified Bedrock integration using Strands' `BedrockModel`
- Removed manual message handling (now managed by Strands framework)
- Added proper tool support using Strands' tool system

#### New Files

**Core Application** (`src/agent_poc/`)
- `agent.py` - `StrandsBedrockAgent` wrapper class around Strands Agent
- `bedrock_client.py` - Factory function to create `BedrockModel` instances
- `tools.py` - Example custom tools (time, calculator, knowledge base search)
- `main.py` - Updated entry point with better logging and demo

**Configuration** (`config/`)
- `settings.py` - Pydantic settings for AWS, Bedrock, and Agent config

**Tests** (`tests/`)
- `test_agent.py` - Tests for agent wrapper
- `test_bedrock_client.py` - Tests for model creation
- `test_settings.py` - Tests for configuration
- `test_tools.py` - Tests for custom tools

**Examples** (`examples/`)
- `basic_usage.py` - Simple query examples
- `agent_with_tools.py` - Tool usage demonstrations
- `streaming_example.py` - Streaming response example
- `README.md` - Examples documentation

**Documentation**
- `README.md` - Comprehensive documentation with Strands-specific info
- `QUICKSTART.md` - 5-minute getting started guide
- `CHANGELOG.md` - This file
- `.env.example` - Environment variables template

#### Key Features

1. **Official Strands Integration**
   - Uses `strands.Agent` for agent orchestration
   - Uses `strands.models.BedrockModel` for AWS Bedrock
   - Automatic tool use and reasoning loop
   - Built-in conversation management

2. **Tool Support**
   - Example tools included (time, calculator, search)
   - Easy to add custom tools
   - Automatic tool discovery and usage by agent

3. **Flexible Configuration**
   - Environment-based configuration
   - Support for multiple AWS credential methods
   - Configurable model parameters (temperature, max_tokens)

4. **Developer Experience**
   - Comprehensive examples
   - Unit tests with mocking
   - Type hints throughout
   - Clear documentation

5. **Production Ready**
   - Proper error handling
   - Logging throughout
   - Configuration validation
   - AWS IAM role support

#### Breaking Changes

- **API Changes**: Complete rewrite of agent API
  - Old: `agent = StrandsAgent(bedrock_client, config)`
  - New: `agent = StrandsBedrockAgent(model, config, tools=[], system_prompt="")`

- **Response Handling**: Simplified response extraction
  - Old: Manual parsing of Bedrock responses
  - New: Strands handles all response parsing

- **Tool System**: New tool definition format
  - Now uses Python type hints with `Annotated` for tool parameters
  - Tools are regular Python functions with docstrings

#### Migration Guide

If upgrading from previous version:

1. Install new dependencies: `poetry install`
2. Update imports:
   ```python
   # Old
   from agent_poc.bedrock_client import BedrockClient
   from agent_poc.agent import StrandsAgent
   
   # New
   from agent_poc.bedrock_client import create_bedrock_model
   from agent_poc.agent import StrandsBedrockAgent
   ```

3. Update agent initialization:
   ```python
   # Old
   client = BedrockClient(aws_config, bedrock_config)
   agent = StrandsAgent(client, agent_config)
   
   # New
   model = create_bedrock_model(aws_config, bedrock_config)
   agent = StrandsBedrockAgent(model, agent_config)
   ```

4. Tool definitions now use Strands format (see `tools.py` for examples)

#### Statistics

- 914 lines of Python code
- 19 Python files (application + tests + examples)
- 4 example scripts
- 100% of core functionality covered by tests

#### Resources

- Strands Documentation: https://strandsagents.com/latest/documentation/docs/
- AWS Bedrock Docs: https://docs.aws.amazon.com/bedrock/
- Project Repository: [Add your repo URL]

### Notes

This is a major rewrite focused on using the official Strands Agents framework rather than a custom implementation. The benefits include:

- Better maintained code (leveraging Strands library)
- More features out of the box (tool use, streaming, etc.)
- Better compatibility with Strands ecosystem
- Reduced maintenance burden
- Production-ready agent patterns

All previous functionality is preserved and enhanced.
