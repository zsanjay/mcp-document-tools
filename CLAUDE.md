# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python package implementing document-related tools (conversion/processing), exposed through an MCP server (`mcp[cli]`, via `FastMCP`) for use by AI assistants.

## Setup & commands

```bash
# Create a virtual env and activate it
uv venv
source .venv/bin/activate

# Install the package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

This project uses `uv` for env/dependency management (see `uv.lock`, `pyproject.toml`) — prefer `uv run <cmd>` / `uv pip ...` over invoking `python`/`pip` directly.

## Architecture

- `main.py` — entry point. Creates a `FastMCP("docs")` server instance and registers tool functions onto it; running the module (`mcp.run()`) starts the MCP server.
- `tools/` — plain Python functions implementing tool logic (e.g. `tools/math.py`, `tools/document.py`). These are independent of MCP — no decorators, no server code — and only become callable MCP tools once explicitly registered in `main.py`.
- `tests/` — pytest tests for the functions in `tools/`, importing them directly (not through the MCP server). `tests/fixtures/` holds binary sample files (`.docx`, `.pdf`) used by document-conversion tests.

**Registration is manual and separate from definition.** A function existing in `tools/` does not mean it's exposed via MCP — check `main.py` for the actual `mcp.tool()(...)` registration calls to see which tools are live. (As of now, only `add` from `tools/math.py` is registered; `binary_document_to_markdown` in `tools/document.py` is defined and tested but not yet wired up in `main.py`.)

`tools/document.py`'s conversion logic wraps the `markitdown` library (`MarkItDown().convert(...)` with a `StreamInfo` for the file extension) to turn binary document data (docx, pdf, etc.) into markdown text.

## Defining new MCP tools

Per the project README, when adding a tool:

1. Write it as a plain Python function in the appropriate module under `tools/`.
2. Register it with the server in `main.py`:
   ```python
   mcp.tool()(my_function)
   ```
3. Use `Field` from `pydantic` to describe each parameter (shown to the AI assistant calling the tool):
   ```python
   from pydantic import Field

   def my_tool(
       param1: str = Field(description="Detailed description of this parameter"),
       param2: int = Field(description="Explain what this parameter does")
   ) -> ReturnType:
       """Comprehensive docstring here"""
       # Implementation
   ```
4. Write the docstring to double as the tool description shown to the assistant. It should:
   - Begin with a one-line summary
   - Provide a detailed explanation of functionality
   - Explain when to use (and not use) the tool
   - Include usage examples with expected input/output (see `add` in `tools/math.py` for the pattern, including doctest-style examples)
