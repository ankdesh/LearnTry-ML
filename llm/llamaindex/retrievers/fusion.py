from typing import List, Any
from llama_index.core.retrievers import BaseRetriever

try:
    from llama_index.core.retrievers import QueryFusionRetriever as LibQueryFusionRetriever
except ImportError:
    LibQueryFusionRetriever = None

class FusionRetriever:
    """
    Wrapper for QueryFusionRetriever.
    """
    def __new__(cls, retrievers: List[BaseRetriever], **kwargs: Any):
        if LibQueryFusionRetriever is None:
            raise ImportError("QueryFusionRetriever not available.")
        
        return LibQueryFusionRetriever(
            retrievers=retrievers,
            **kwargs
        )
