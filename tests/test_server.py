import json
import pytest
from mcp_reranker.server import rerank_documents

def test_rerank_documents_basic():
    """正常系のテスト: クエリに対して関連度の高いドキュメントが上位に来るか検証"""
    query = "Python programming"
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a high-level, general-purpose programming language.",
        "I like eating apples and bananas.",
        "FastAPI is a modern, fast web framework for building APIs with Python."
    ]
    
    # ツールの実行
    result_str = rerank_documents(query, documents)
    result = json.loads(result_str)
    
    # 戻り値の構造と件数の確認
    assert len(result) == 4
    assert "document" in result[0]
    assert "score" in result[0]
    
    # 関連度の高いドキュメントが上位（0番目か1番目）に来ているか
    top_doc = result[0]["document"].lower()
    assert "python" in top_doc

def test_rerank_documents_empty_documents():
    """異常系/境界値のテスト: 空のドキュメントリストが渡された場合"""
    query = "Test query"
    documents = []
    
    # ツールの実行
    result_str = rerank_documents(query, documents)
    result = json.loads(result_str)
    
    # 空のリストが返ることを確認
    assert result == []
    assert len(result) == 0