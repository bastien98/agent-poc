"""Custom tools for the Strands agent.

This module provides example tools that can be used with the Strands agent.
Tools allow the agent to perform actions and retrieve information beyond its base knowledge.
"""

import logging
from datetime import datetime
from typing import Annotated, List, Optional
import boto3
from botocore.exceptions import ClientError

from agent_poc.config.settings import get_settings

logger: logging.Logger = logging.getLogger(__name__)


def get_current_time() -> str:
    """Get the current time.
    
    Returns:
        Current time in ISO format
    """
    logger.info("Tool called: get_current_time")
    current_time: str = datetime.now().isoformat()
    return current_time


def calculate(
    expression: Annotated[str, "A mathematical expression to evaluate"]
) -> str:
    """Safely evaluate a simple mathematical expression.
    
    Args:
        expression: A mathematical expression (e.g., "2 + 2", "10 * 5")
        
    Returns:
        The result of the calculation as a string
        
    Raises:
        Exception: If the expression is invalid or contains unsafe characters
    """
    logger.info(f"Tool called: calculate with expression: {expression}")
    
    try:
        # Only allow safe operations
        allowed_chars: set[str] = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        
        # Evaluate safely
        result: float = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return f"Error: {str(e)}"


def query_bedrock_knowledge_base(
    query: Annotated[str, "The search query to search the knowledge base"],
    max_results: Annotated[int, "Maximum number of results to return (default: 5)"] = 5
) -> str:
    """Query an AWS Bedrock Knowledge Base for information.
    
    This tool connects to an AWS Bedrock Knowledge Base and retrieves relevant
    information based on the provided query. The knowledge base uses vector search
    to find the most relevant documents.
    
    Args:
        query: The search query to find relevant information
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Retrieved information from the knowledge base, formatted as text
        
    Raises:
        Exception: If there's an error querying the knowledge base
    """
    logger.info(f"Tool called: query_bedrock_knowledge_base with query: {query}")
    
    try:
        # Load settings
        settings = get_settings()
        
        # Check if KB ID is configured
        if not settings.bedrock_kb.bedrock_kb_id:
            return "Error: Bedrock Knowledge Base ID is not configured. Please set BEDROCK_KB_ID in your .env file."
        
        # Initialize the Bedrock Agent Runtime client
        session = boto3.Session(
            aws_access_key_id=settings.aws.aws_access_key_id,
            aws_secret_access_key=settings.aws.aws_secret_access_key,
            aws_session_token=settings.aws.aws_session_token,
            region_name=settings.bedrock_kb.bedrock_kb_region
        )
        
        bedrock_agent_runtime = session.client('bedrock-agent-runtime')
        
        # Query the knowledge base
        logger.info(f"Querying KB ID: {settings.bedrock_kb.bedrock_kb_id}")
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=settings.bedrock_kb.bedrock_kb_id,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': max_results
                }
            }
        )
        
        # Extract and format results
        retrieval_results = response.get('retrievalResults', [])
        
        if not retrieval_results:
            return f"No results found in the knowledge base for query: '{query}'"
        
        # Format the results
        formatted_results = []
        for i, result in enumerate(retrieval_results, 1):
            content = result.get('content', {}).get('text', 'No content available')
            score = result.get('score', 0.0)
            location = result.get('location', {})
            
            # Extract source information
            source_info = ""
            if location.get('type') == 'S3':
                s3_location = location.get('s3Location', {})
                source_info = f"Source: s3://{s3_location.get('uri', 'unknown')}"
            
            formatted_results.append(
                f"Result {i} (relevance: {score:.2f}):\n"
                f"{content}\n"
                f"{source_info}\n"
            )
        
        result_text = "\n".join(formatted_results)
        logger.info(f"Successfully retrieved {len(retrieval_results)} results from knowledge base")
        
        return f"Knowledge Base Search Results for '{query}':\n\n{result_text}"
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS ClientError: {error_code} - {error_message}")
        return f"Error querying knowledge base: {error_code} - {error_message}"
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}", exc_info=True)
        return f"Error querying knowledge base: {str(e)}"


def search_knowledge_base(
    query: Annotated[str, "The search query"]
) -> str:
    """Search a knowledge base for information.
    
    This is a placeholder that would integrate with a real knowledge base or RAG system.
    
    Args:
        query: The search query
        
    Returns:
        Search results or relevant information
    """
    logger.info(f"Tool called: search_knowledge_base with query: {query}")
    
    # Placeholder implementation
    result: str = (
        f"This is a placeholder for knowledge base search results for query: '{query}'. "
        "In a production system, this would search a vector database, "
        "document store, or other knowledge repository."
    )
    return result


# Export all tools
__all__: List[str] = [
    "get_current_time",
    "calculate",
    "query_bedrock_knowledge_base",
    "search_knowledge_base",
]
