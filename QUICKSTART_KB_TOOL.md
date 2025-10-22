# Quick Start: Bedrock Knowledge Base Tool

## 1. Configure (2 minutes)

Edit `.env`:
```bash
BEDROCK_KB_ID=YOUR_KB_ID_HERE
BEDROCK_KB_REGION=us-east-1
```

Find your KB ID: AWS Console → Bedrock → Knowledge bases → Copy ID

## 2. Test Connection (1 minute)

```bash
cd examples
python test_kb_tool.py
```

Enter a test query when prompted.

## 3. Use with Agent (2 minutes)

```python
from agent_poc.tools import query_bedrock_knowledge_base
from agent_poc.agent import StrandsAgent
from agent_poc.openai_client import create_openai_model
from agent_poc.config.settings import get_settings

settings = get_settings()
model = create_openai_model(settings.openai)

agent = StrandsAgent(
    model=model,
    config=settings.agent,
    tools=[query_bedrock_knowledge_base]
)

# Agent automatically uses KB when needed
response = agent.run("What documentation do you have?")
print(response)
```

## 4. Run Full Example

```bash
python kb_query_example.py
```

## Troubleshooting

**No KB ID configured?**
→ Set `BEDROCK_KB_ID` in `.env`

**Access denied?**
→ Add IAM permission: `bedrock:Retrieve`

**KB not found?**
→ Check region matches KB location

## Need More Help?

📖 Full docs: `KB_TOOL_README.md`  
📋 Summary: `KB_TOOL_SUMMARY.md`

Done! 🎉
