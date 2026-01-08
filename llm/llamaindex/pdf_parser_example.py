
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

try:
    from docling.document_converter import DocumentConverter
    from docling.chunking import HybridChunker
    from llama_index.core import VectorStoreIndex, Document
    from llama_index.core.node_parser import NodeParser
    from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
    from llama_index.core.retrievers import RecursiveRetriever
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def main():
    pdf_path = Path("sample.pdf")
    if not pdf_path.exists():
        print(f"File {pdf_path} not found.")
        return

    # 1. Convert PDF using Docling
    print("Converting PDF...")
    converter = DocumentConverter()
    doc_result = converter.convert(pdf_path)
    doc = doc_result.document
    
    # 2. Chunking using HybridChunker
    print("Chunking document...")
    chunker = HybridChunker(
        tokenizer="sentence-transformers/all-MiniLM-L6-v2" # Optional, purely for token counting if needed
    ) 
    # Note: Check if HybridChunker needs arguments or if defaults work.
    chunk_iter = chunker.chunk(doc)
    chunks = list(chunk_iter)
    
    print(f"Generated {len(chunks)} chunks.")

    # 3. Convert to LlamaIndex Nodes
    print("Creating LlamaIndex Nodes...")
    nodes = []
    if chunks:
        print(f"First chunk metadata: {chunks[0].meta}")
        try:
            print(f"First chunk metadata vars: {vars(chunks[0].meta)}")
        except:
            pass
            
    for i, chunk in enumerate(chunks):
        # Docling chunks have text and metadata (including headers)
        # Inspect structure from logs
        page_num = None
        # Try to find page number safely
        # It might be in chunk.meta.origin.page_references[0].page_no?
        
        # Temporary fix: simple safely get or default
        # metadata={
        #     "page": chunk.meta.page.page_no if chunk.meta.page else None,
        #     "headings": [h.text for h in chunk.meta.headings] if chunk.meta.headings else []
        # }
        
        # Let's clean up the access based on assumption it might be nested
        # For now, let's just dump meta as dict if possible or use safe access
        node_meta = {}
        if hasattr(chunk.meta, "headings") and chunk.meta.headings:
             node_meta["headings"] = [h for h in chunk.meta.headings] # might be strings or objects

        node = TextNode(
            text=chunk.text,
            metadata=node_meta
        )
        nodes.append(node)

    # 4. Setup LlamaIndex for RecursiveRetrieval
    # RecursiveRetriever usually works by having a set of nodes indexed, and maybe some references.
    # For this example, let's index all nodes.
    # To demonstrate "Recursive" nature, we might technically need references which point to other nodes (like summaries pointing to raw),
    # but here we simply show we can build the retriever.
    
    # Use a local embedding model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    index = VectorStoreIndex(
        nodes, 
        embed_model=embed_model
    )
    
    # "RecursiveRetriever" needs a retrieval strategy.
    # Often it wraps another retriever (like VectorStoreRetriever) and traverses references.
    # If we don't have references (NodeRelationship.SOURCE pointing to something else explicitly added to 'all_nodes_dict'),
    # it behaves like a standard retriever or we need to configure it.
    
    # Let's create a dictionary of all nodes to pass to RecursiveRetriever if we wanted so.
    all_nodes_dict = {n.node_id: n for n in nodes}
    
    vector_retriever = index.as_retriever(similarity_top_k=3)
    
    recursive_retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": vector_retriever},
        # node_dict=all_nodes_dict, # Only needed if we have nodes that reference other nodes by ID but aren't in the index
        verbose=True
    )
    
    # 5. Query
    query = "What is the main topic of this document?"
    print(f"\nQuerying: {query}")
    
    retrieved_nodes = recursive_retriever.retrieve(query)
    
    print(f"\nRetrieved {len(retrieved_nodes)} nodes:")
    for node in retrieved_nodes:
        print("-" * 20)
        print(f"Score: {node.score}")
        print(f"Text: {node.get_content()[:200]}...")
        print(f"Metadata: {node.metadata}")

if __name__ == "__main__":
    main()
