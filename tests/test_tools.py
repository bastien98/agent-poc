"""Tests for agent tools."""

import pytest
from agent_poc.tools import get_current_time, calculate, search_knowledge_base


def test_get_current_time():
    """Test get_current_time tool."""
    result = get_current_time()
    assert isinstance(result, str)
    # Should be ISO format
    assert "T" in result


def test_calculate_simple():
    """Test simple calculation."""
    result = calculate("2 + 2")
    assert result == "4"


def test_calculate_complex():
    """Test complex calculation."""
    result = calculate("(10 + 5) * 2")
    assert result == "30"


def test_calculate_invalid_chars():
    """Test calculation with invalid characters."""
    result = calculate("import os")
    assert "Error" in result
    assert "invalid characters" in result


def test_calculate_division():
    """Test division calculation."""
    result = calculate("10 / 2")
    assert result == "5.0"


def test_calculate_error():
    """Test calculation error handling."""
    result = calculate("1 / 0")
    assert "Error" in result


def test_search_knowledge_base():
    """Test knowledge base search tool."""
    result = search_knowledge_base("test query")
    assert isinstance(result, str)
    assert "test query" in result
    assert "placeholder" in result.lower()
