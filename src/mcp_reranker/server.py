import json
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from sentence_transformers import CrossEncoder

# サーバーの初期化
mcp = FastMCP("mcp-reranker")

# モデルのキャッシュ用辞書
_rerankers: Dict[str, CrossEncoder] = {}

def get_reranker(model_name: str) -> CrossEncoder:
    """指定されたモデルをロードしてキャッシュから返す"""
    if model_name not in _rerankers:
        _rerankers[model_name] = CrossEncoder(model_name)
    return _rerankers[model_name]

@mcp.tool()
def rerank_documents(query: str, documents: List[str], model_name: str = "BAAI/bge-reranker-v2-m3") -> str:
    """
    Reranks a list of documents based on their relevance to a given query.
    
    Args:
        query: The core intent or query string to compare against.
        documents: A list of document descriptions/strings to be ranked.
        model_name: The HuggingFace model name for the CrossEncoder. Default is 'BAAI/bge-reranker-v2-m3'.
        
    Returns:
        A JSON string representing a sorted list of dictionaries containing 'document' and 'score'.
    """
    if not documents:
        return json.dumps([])
        
    reranker = get_reranker(model_name)
    
    # 比較ペアの作成
    pairs = [[query, doc] for doc in documents]
    
    # スコアの予測
    scores = reranker.predict(pairs)
    
    # 結果の整形とソート
    results = [{"document": doc, "score": float(score)} for doc, score in zip(documents, scores)]
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return json.dumps(results, ensure_ascii=False)

def main():
    # MCPサーバーの起動
    mcp.run()

if __name__ == "__main__":
    main()