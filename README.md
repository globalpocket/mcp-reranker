# mcp-reranker

A generic [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides document reranking capabilities using `sentence-transformers`.

This server is designed to be a standalone tool that can be used by any MCP-compatible client (such as Roo Code, Claude Desktop, or custom agents) to improve the precision of RAG (Retrieval-Augmented Generation) or to help agents make better decisions by scoring relevance between a query and multiple candidates.

## Features

- **Cross-Encoder Reranking**: Utilizes the `CrossEncoder` model from `sentence-transformers` for high-accuracy relevance scoring.
- **Project Agnostic**: Completely independent of any specific application logic.
- **Customizable Models**: Supports various HuggingFace models. You can configure the default model via environment variables (defaults to `BAAI/bge-reranker-v2-m3`).
- **JSON Output**: Returns sorted results in a structured JSON format.

## Tools

### `rerank_documents`

Computes relevance scores for a list of documents against a given query and returns them sorted by score.

**Arguments:**

- `query` (string): The search query or the core intent to compare against.
- `documents` (array of strings): A list of document descriptions or texts to be ranked.
- `model_name` (string, optional): The HuggingFace model identifier. Defaults to the `RERANKER_MODEL_NAME` environment variable or `"BAAI/bge-reranker-v2-m3"`.

**Response Example:**
A JSON-formatted string:

```json
[
  { "document": "The most relevant document text.", "score": 0.985 },
  { "document": "A partially relevant text.", "score": 0.452 },
  { "document": "Completely irrelevant text.", "score": 0.012 }
]
```

## Installation & Usage

### Running with `uvx`

Add the following to your MCP configuration (e.g., `brownie_core_mcp_config.json`). 
You can customize the model used by setting the `RERANKER_MODEL_NAME` environment variable.

```json
{
  "mcpServers": {
    "mcp-reranker": {
      "command": "uvx",
      "args": [
        "--from",
        "git+[https://github.com/globalpocket/mcp-reranker.git](https://github.com/globalpocket/mcp-reranker.git)",
        "mcp-reranker"
      ],
      "env": {
        "RERANKER_MODEL_NAME": "BAAI/bge-reranker-v2-m3"
      }
    }
  }
}
```

## Development

### Prerequisites

- Python 3.10+
- [uv](https://astral.sh/uv/)

### Setup

```bash
git clone [https://github.com/globalpocket/mcp-reranker.git](https://github.com/globalpocket/mcp-reranker.git)
cd mcp-reranker
uv sync --extra dev
```

### Running Tests

```bash
uv run pytest
```

## License

MIT License
