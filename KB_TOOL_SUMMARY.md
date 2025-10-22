# Bedrock Knowledge Base Tool - Quick Summary

## What was created

A tool that allows your Strands agent to query AWS Bedrock Knowledge Bases for information retrieval.

## Files Added/Modified

### New Files
1. **`KB_TOOL_README.md`** - Complete documentation for the KB tool
2. **`examples/kb_query_example.py`** - Example of using the tool with an agent
3. **`examples/test_kb_tool.py`** - Standalone tool tester

### Modified Files
1. **`src/agent_poc/tools.py`** - Added `query_bedrock_knowledge_base()` function
2. **`src/agent_poc/config/settings.py`** - Added `BedrockKnowledgeBaseConfig` class
3. **`.env`** - Added `BEDROCK_KB_ID` and `BEDROCK_KB_REGION` configuration
4. **`.env.example`** - Updated with KB configuration examples

## Configuration Required

Add to your `.env` file:

```bash
# AWS Bedrock Knowledge Base Configuration
BEDROCK_KB_ID=your_actual_kb_id_here
BEDROCK_KB_REGION=us-east-1
```

You'll also need AWS credentials with `bedrock:Retrieve` permissions.

## Usage

### Quick Test
```bash
cd examples
python test_kb_tool.py
```

### With Agent
```python
from agent_poc.tools import query_bedrock_knowledge_base
from agent_poc.agent import StrandsAgent

agent = StrandsAgent(
    model=model,
    config=config,
    tools=[query_bedrock_knowledge_base],
    system_prompt="Use the KB to answer questions."
)

response = agent.run("What information do you have about pricing?")
```

### Full Example
```bash
cd examples
python kb_query_example.py
```

## Tool Function

```python
def query_bedrock_knowledge_base(
    query: str,
    max_results: int = 5
) -> str:
    """Query AWS Bedrock Knowledge Base.
    
    Args:
        query: Search query
        max_results: Max number of results (default: 5)
    
    Returns:
        Formatted search results with sources
    """
```

## Key Features

✅ **Vector Search**: Uses Bedrock's vector search for semantic matching  
✅ **Source Citations**: Returns source information (S3 URIs) for each result  
✅ **Relevance Scores**: Shows similarity scores for each retrieved document  
✅ **Error Handling**: Graceful error messages for common issues  
✅ **Configurable**: Adjustable result count and region settings  
✅ **Multi-Provider**: Works with both OpenAI and Bedrock models  

## Next Steps

1. **Configure your KB ID** in `.env`
2. **Test the connection** with `test_kb_tool.py`
3. **Try the example** with `kb_query_example.py`
4. **Integrate into your workflows** using the agent

## Documentation

See **`KB_TOOL_README.md`** for:
- Detailed setup instructions
- IAM permissions required
- Troubleshooting guide
- Best practices
- Advanced usage examples

## Common Issues

| Issue | Solution |
|-------|----------|
| "KB ID is not configured" | Set `BEDROCK_KB_ID` in `.env` |
| "AccessDeniedException" | Add `bedrock:Retrieve` IAM permission |
| "ResourceNotFoundException" | Verify KB ID and region are correct |
| No results | Check KB has synced documents |

## Cost Considerations

- Each KB query incurs AWS charges
- Monitor usage in AWS Cost Explorer
- Consider caching frequent queries
- Use appropriate `max_results` values

## Example Output

```
Knowledge Base Search Results for 'API documentation':

Result 1 (relevance: 0.89):
The API supports RESTful endpoints for user management...
Source: s3://docs-bucket/api/user-management.pdf

Result 2 (relevance: 0.76):
Authentication is handled via OAuth 2.0 tokens...
Source: s3://docs-bucket/api/authentication.pdf
```
