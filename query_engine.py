
from dotenv import load_dotenv
load_dotenv()
import llama_index.core
from llama_index.core import VectorStoreIndex
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from vector_stores import VectorStore3A
from utils import load_and_chunk_docx

llama_index.core.set_global_handler("simple")

FILEPATH = "Payment_Cards.docx"

# Load the file and chunk it
nodes = load_and_chunk_docx(FILEPATH)

# Get embeddings for each chunk
embed_model = HuggingFaceEmbedding()
for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding


# Create vector store (in-memory)
vector_store = VectorStore3A()
vector_store.add(nodes)

# Create index using vector store
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=HuggingFaceEmbedding())


# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=1,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

# Init the query engine
query_engine = index.as_query_engine()



