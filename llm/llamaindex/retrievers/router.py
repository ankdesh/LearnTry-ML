from typing import List, Any, Optional
from llama_index.core.retrievers import RouterRetriever as LibRouterRetriever
from llama_index.core.tools import RetrieverTool
from llama_index.core.selectors import BaseSelector, LLMSingleSelector

class RouterRetriever:
    """
    Wrapper for RouterRetriever.
    """
    def __new__(cls, retriever_tools: List[RetrieverTool], selector: Optional[BaseSelector] = None, **kwargs: Any):
        
        if selector is None:
             # Fallback if not provided.
             # Note: This might require LLM setup in environment
             selector = LLMSingleSelector.from_defaults()

        return LibRouterRetriever(
            selector=selector,
            retriever_tools=retriever_tools,
            **kwargs
        )
