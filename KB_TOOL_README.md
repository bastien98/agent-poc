# Bedrock Knowledge Base Tool

This tool allows the Strands agent to query an AWS Bedrock Knowledge Base to retrieve relevant information based on user queries.

## Overview

The `query_bedrock_knowledge_base` tool connects to AWS Bedrock Knowledge Bases and uses vector search to find the most relevant documents for a given query. This enables the agent to access enterprise knowledge, documentation, or any content indexed in your Knowledge Base.

## Setup

### 1. Configure AWS Credentials

Add your AWS credentials to the `.env` file:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=optional_session_token  # Only if using temporary credentials
```

Alternatively, you can use AWS CLI default credentials (profile, IAM role, etc.).

### 2. Configure Knowledge Base

Add your Bedrock Knowledge Base ID to the `.env` file:

```bash
# AWS Bedrock Knowledge Base Configuration
BEDROCK_KB_ID=YOUR_KNOWLEDGE_BASE_ID_HERE
BEDROCK_KB_REGION=us-east-1  # Region where your KB is deployed
```

**Finding your Knowledge Base ID:**
1. Go to the AWS Console
2. Navigate to Amazon Bedrock > Knowledge bases
3. Select your knowledge base
4. Copy the "Knowledge base ID" (format: ABCD1234EFGH)

### 3. IAM Permissions

Your AWS credentials need the following IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": "arn:aws:bedrock:*:*:knowledge-base/*"
        }
    ]
}
```

## Usage

### Direct Tool Usage

Test the tool directly without the agent:

```bash
cd examples
python test_kb_tool.py
```

This will prompt you for a test query and display the results.

### With the Agent

Use the tool with the Strands agent:

```python
from agent_poc.tools import query_bedrock_knowledge_base
from agent_poc.agent import StrandsAgent

# Initialize agent with the KB tool
agent = StrandsAgent(
    model=model,
    config=config,
    tools=[query_bedrock_knowledge_base],
    system_prompt="Use the knowledge base tool to answer questions."
)

# The agent will automatically use the tool when needed
response = agent.run("What information do you have about product features?")
```

### Example Script

Run the complete example:

```bash
cd examples
python kb_query_example.py
```

## Tool Parameters

### `query_bedrock_knowledge_base(query, max_results=5)`

**Parameters:**
- `query` (str, required): The search query to find relevant information
- `max_results` (int, optional): Maximum number of results to return (default: 5)

**Returns:**
- String containing formatted search results with relevance scores and sources

**Example:**
```python
result = query_bedrock_knowledge_base(
    query="What are the API rate limits?",
    max_results=3
)
print(result)
```

## Output Format

The tool returns results in the following format:

```
Knowledge Base Search Results for 'your query':

Result 1 (relevance: 0.85):
[Document content...]
Source: s3://bucket-name/path/to/document.pdf

Result 2 (relevance: 0.72):
[Document content...]
Source: s3://bucket-name/path/to/other-doc.pdf
```

## Troubleshooting

### Error: "Bedrock Knowledge Base ID is not configured"
- Make sure `BEDROCK_KB_ID` is set in your `.env` file
- Verify the `.env` file is in the project root directory

### Error: "AccessDeniedException"
- Check that your AWS credentials are correct
- Verify your IAM user/role has `bedrock:Retrieve` permissions
- Ensure the Knowledge Base exists in the specified region

### Error: "ResourceNotFoundException"
- Verify the Knowledge Base ID is correct
- Check that the Knowledge Base is in the region specified in `BEDROCK_KB_REGION`
- Ensure the Knowledge Base is in "Available" state (not creating/updating)

### No Results Returned
- The Knowledge Base might not contain relevant documents for your query
- Try broader or more specific queries
- Check the Knowledge Base sync status in AWS Console

## Integration with Different Providers

The tool works with both OpenAI and Bedrock model providers:

### With OpenAI
```python
from agent_poc.openai_client import create_openai_model

model = create_openai_model(settings.openai)
agent = StrandsAgent(
    model=model,
    tools=[query_bedrock_knowledge_base],
    ...
)
```

### With Bedrock
```python
from agent_poc.bedrock_client import create_bedrock_model

model = create_bedrock_model(settings.aws, settings.bedrock)
agent = StrandsAgent(
    model=model,
    tools=[query_bedrock_knowledge_base],
    ...
)
```

## Best Practices

1. **Specific Queries**: Encourage specific, well-formed queries for better results
2. **Result Limits**: Adjust `max_results` based on your use case (fewer for focused queries, more for exploratory searches)
3. **Source Citations**: The tool includes source information - use this in your responses to users
4. **Error Handling**: The tool gracefully handles errors and returns descriptive error messages
5. **Cost Optimization**: Knowledge Base queries incur costs - monitor usage in AWS Cost Explorer

## Advanced Usage

### Custom System Prompt

Guide the agent on when and how to use the KB:

```python
system_prompt = """
You are a helpful assistant with access to a company knowledge base.
When users ask questions about:
- Products and features
- Documentation
- Policies and procedures
- Technical specifications

Always use the query_bedrock_knowledge_base tool to find accurate, up-to-date information.
Cite your sources using the source information provided.
If the knowledge base doesn't have relevant information, say so clearly.
"""
```

### Combining Multiple Tools

Use the KB tool alongside other tools:

```python
from agent_poc.tools import (
    query_bedrock_knowledge_base,
    get_current_time,
    calculate
)

agent = StrandsAgent(
    model=model,
    tools=[
        query_bedrock_knowledge_base,  # For knowledge retrieval
        get_current_time,              # For temporal context
        calculate                       # For calculations
    ],
    ...
)
```

## Example Queries

Good queries for knowledge bases:

- "What are the system requirements for the application?"
- "Find documentation about the authentication API"
- "What is the company's return policy?"
- "Search for information about data retention policies"
- "What are the available pricing tiers?"

## Next Steps

1. Test the tool with `test_kb_tool.py`
2. Run the example with `kb_query_example.py`
3. Integrate into your own agent workflows
4. Customize the system prompt for your use case
5. Monitor usage and costs in AWS Console

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review AWS Bedrock Knowledge Base documentation
3. Verify your Knowledge Base is properly configured and synced
4. Check CloudWatch logs for detailed error messages
