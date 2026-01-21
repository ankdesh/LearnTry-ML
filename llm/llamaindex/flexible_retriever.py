from typing import Dict, Any, List, Optional
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.tools import RetrieverTool

# Import new separate implementations
from retrievers.vector import VectorRetriever
from retrievers.bm25 import BM25Retriever
from retrievers.fusion import FusionRetriever
from retrievers.router import RouterRetriever

class FlexibleRetriever(BaseRetriever):
    """
    A binding class that configures and delegates to specific retriever implementations.
    """

    def __init__(
        self,
        index: VectorStoreIndex,
        config: Dict[str, Any],
        custom_retrievers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Args:
            index: The default VectorStoreIndex.
            config: Configuration dictionary.
            custom_retrievers: Registry of custom retriever classes or instances.
        """
        self._index = index
        self._custom_retrievers = custom_retrievers or {}
        self._retriever = self._build_retriever(config)
        super().__init__()

    def _build_retriever(self, config: Dict[str, Any]) -> BaseRetriever:
        name = config.get("name")
        params = config.get("params", {})
        
        # 1. Custom Retrievers
        if name in self._custom_retrievers:
            custom_cls_or_obj = self._custom_retrievers[name]
            if isinstance(custom_cls_or_obj, type):
                 return custom_cls_or_obj(**params)
            else:
                return custom_cls_or_obj

        # 2. Standard Retrievers
        if name == "vector":
            return VectorRetriever(index=self._index, **params)

        if name == "bm25":
            return BM25Retriever(index=self._index, **params)

        if name == "query_fusion":
            # Recursively build sub-retrievers
            sub_configs = config.get("retrievers", [])
            sub_retrievers = [self._build_retriever(c) for c in sub_configs]
            return FusionRetriever(retrievers=sub_retrievers, **params)

        if name == "router":
            # Recursively build sub-retrievers and wrap in tools
            sub_configs = config.get("retrievers", [])
            retriever_tools = []
            for c in sub_configs:
                retriever = self._build_retriever(c)
                description = c.get("description", "A retriever.")
                tool_name = c.get("tool_name", f"retriever_{len(retriever_tools)}")
                
                retriever_tools.append(
                    RetrieverTool.from_defaults(
                        retriever=retriever,
                        description=description,
                        name=tool_name
                    )
                )
            
            selector = params.pop("selector", None)
            return RouterRetriever(retriever_tools=retriever_tools, selector=selector, **params)

        raise ValueError(f"Unknown retriever name: {name}")

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        return self._retriever.retrieve(query_bundle)

