from typing import Any
from llama_index.core import VectorStoreIndex

try:
    from llama_index.retrievers.bm25 import BM25Retriever as LibBM25Retriever
except ImportError:
    LibBM25Retriever = None

class BM25Retriever:
    """
    Wrapper for BM25Retriever.
    Serves as a factory/wrapper to handle the import check and initialization from index.
    """
    def __new__(cls, index: VectorStoreIndex, **kwargs: Any):
        if LibBM25Retriever is None:
            raise ImportError("BM25Retriever is not available. Please install 'rank_bm25'.")
        
        # We assume initialization from index defaults as per original implementation
        return LibBM25Retriever.from_defaults(index=index, **kwargs)
