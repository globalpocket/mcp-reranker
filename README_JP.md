# mcp-reranker

`sentence-transformers` を使用して、クエリと文書の関連度を再計算（Rerank）する汎用 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) サーバーです。

このサーバーは特定のプロジェクトに依存しない独立したツールとして設計されており、Roo Code、Claude Desktop、または自作のエージェントなど、あらゆる MCP 対応クライアントから利用可能です。RAG（検索拡張生成）の精度向上や、エージェントが複数の候補から最適な回答を選択する際の補助に役立ちます。

## 特徴

- **Cross-Encoder による高精度な判定**: `sentence-transformers` の `CrossEncoder` を使用し、単純なベクトル検索よりも高精度な関連度スコアリングを提供します。
- **完全な汎用性**: BROWNIE などの特定のエージェントロジックに依存せず、純粋な計算リソースとして動作します。
- **モデルの柔軟性**: HuggingFace 上の CrossEncoder モデルを自由に指定可能です。環境変数でデフォルトモデルを設定できます（デフォルト: `BAAI/bge-reranker-v2-m3`）。
- **構造化された出力**: スコア順にソートされた JSON 形式で結果を返します。

## 提供ツール

### `rerank_documents`

指定されたクエリに対する文書リストの関連度スコアを計算し、スコアの高い順にソートして返します。

**引数:**

- `query` (string): 比較の基準となる検索クエリや「意図」。
- `documents` (string の配列): ランク付けを行いたい文書や説明文のリスト。
- `model_name` (string, 任意): 使用する HuggingFace のモデル名。デフォルトは環境変数 `RERANKER_MODEL_NAME`、または `"BAAI/bge-reranker-v2-m3"`。

**レスポンス例:**
以下のような JSON 文字列が返されます。

```json
[
  { "document": "最も関連性の高い文書の内容", "score": 0.985 },
  { "document": "部分的に関連する内容", "score": 0.452 },
  { "document": "無関係な内容", "score": 0.012 }
]
```

## インストールと設定

### `uvx` による実行

MCP 設定ファイル（例: `brownie_core_mcp_config.json`）に以下の設定を追加してください。
環境変数 `RERANKER_MODEL_NAME` を設定することで、使用するモデルを変更できます。

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

## 開発環境

### 動作要件

- Python 3.10以上
- [uv](https://astral.sh/uv/)

### セットアップ

```bash
git clone [https://github.com/globalpocket/mcp-reranker.git](https://github.com/globalpocket/mcp-reranker.git)
cd mcp-reranker
uv sync --extra dev
```

### テストの実行

```bash
uv run pytest
```

## ライセンス

MIT License
