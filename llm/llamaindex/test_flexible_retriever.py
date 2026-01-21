
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM
from llama_index.core.selectors import LLMSingleSelector
from flexible_retriever import FlexibleRetriever

# Setup Mock Settings to avoid OpenAI dependency
Settings.embed_model = MockEmbedding(embed_dim=1536)
Settings.llm = MockLLM()

# Mock class for Custom Retriever
class MyCustomRetriever:
    def __init__(self, mode="default"):
        self.mode = mode

    def retrieve(self, query):
        from llama_index.core.schema import NodeWithScore, TextNode
        return [NodeWithScore(node=TextNode(text=f"Custom result ({self.mode}): {query}"), score=1.0)]

def main():
    # 1. Setup a basic Index
    docs = [
        Document(text="This is written by Shakespeare."),
        Document(text="This is written by Dickens."),
        Document(text="Machine learning is fascinating."),
    ]
    index = VectorStoreIndex.from_documents(docs)

    # 2. Test Vector Config
    print("--- Test Vector Retriever ---")
    config_vector = {
        "name": "vector",
        "params": {"similarity_top_k": 1}
    }
    retriever = FlexibleRetriever(index, config_vector)
    results = retriever.retrieve("Shakespeare")
    print(f"Results: {len(results)}")
    print(results[0].node.text if results else "No results")

    # 3. Test Custom Retriever
    print("\n--- Test Custom Retriever ---")
    config_custom = {
        "name": "my_custom",
        "params": {"mode": "expert"}
    }
    custom_registry = {"my_custom": MyCustomRetriever}
    retriever = FlexibleRetriever(index, config_custom, custom_retrievers=custom_registry)
    results = retriever.retrieve("Test Query")
    print(f"Results: {len(results)}")
    print(results[0].node.text if results else "No results")

    # 4. Test Query Fusion (Mocking dependencies if needed, but assuming installed)
    try:
        from llama_index.core.retrievers import QueryFusionRetriever
        print("\n--- Test Query Fusion (Vector + Vector for demo) ---")
        config_fusion = {
            "name": "query_fusion",
            "params": {"num_queries": 1, "similarity_top_k": 2},
            "retrievers": [
                 {"name": "vector", "params": {"similarity_top_k": 1}},
                 {"name": "vector", "params": {"similarity_top_k": 1}} # just combining two vectors for simple test
            ]
        }
        retriever = FlexibleRetriever(index, config_fusion)
        results = retriever.retrieve("Machine Learning")
        print(f"Results: {len(results)}")
        for r in results:
            print(f"- {r.node.text}")

    except ImportError:
        print("\nSkipping QueryFusion test (missing dependencies)")

    # 5. Test Router Retriever
    print("\n--- Test Router Retriever ---")
    # Router needs a selector. We usually need an LLM for the selector.
    # For this test, we might mock the selector or skip if no LLM configured.
    # We will try to instantiate it at least.
    
    try:
        from llama_index.core.selectors import LLMSingleSelector
        
        # We need a mock LLM or real LLM for the selector to work fully, 
        # but here we just test instantiation and structure.
        config_router = {
            "name": "router",
            "params": {
                "selector": LLMSingleSelector.from_defaults() # This might fail if no LLM, let's see
            },
            "retrievers": [
                {
                    "name": "vector", 
                    "params": {"similarity_top_k": 1},
                    "description": "Useful for finding Shakespeare",
                    "tool_name": "shakespeare_tool"
                },
                 {
                    "name": "vector", 
                    "params": {"similarity_top_k": 1},
                    "description": "Useful for finding Dickens",
                    "tool_name": "dickens_tool"
                }
            ]
        }
        
        # Since we might not have OpenAI/LLM key set up in this env, instantiation usually expects an LLM.
        # LLMSingleSelector.from_defaults() tries to get default LLM.
        # We will wrap in try-except for the run part.
        
        retriever = FlexibleRetriever(index, config_router)
        print("Router Retriever instantiated successfully.")
        
    except Exception as e:
        print(f"Router Test Error (expected if no LLM): {e}")


if __name__ == "__main__":
    main()
