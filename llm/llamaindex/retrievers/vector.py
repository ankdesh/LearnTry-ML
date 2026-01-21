from typing import Any
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

class VectorRetriever(VectorIndexRetriever):
    """
    Wrapper around VectorIndexRetriever to allow initialization 
    with 'params' passed indiscriminately.
    """
    def __init__(self, index: VectorStoreIndex, **kwargs: Any) -> None:
        super().__init__(index=index, **kwargs)
