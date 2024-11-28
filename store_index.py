from src.helper import load_pdf_file, text_split, download_OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Pinecone and OpenAI API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("PINECONE_API_KEY and OPENAI_API_KEY must be set in the environment or .env file")

# Extract data from PDF files
extracted_data = load_pdf_file(data='Data/')

# Split the extracted text into smaller chunks
text_chunks = text_split(extracted_data)

# Download embeddings using OpenAI's embedding model
embeddings = download_OpenAIEmbeddings()

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define and create a Pinecone index
index_name = "medicalbot"
pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Store text chunks as vectorized documents in the Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)
