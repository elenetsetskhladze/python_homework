from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from models import DocumentChunk, Base
from sqlalchemy.orm import Session
from database import engine

Base.metadata.create_all(engine)

client = genai.Client()

loader = UnstructuredMarkdownLoader("hotel_info.md")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=40)

chunks = splitter.split_documents(docs)

texts = [chunk.page_content for chunk in chunks]

result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=texts
)

embedding = [item.values for item in result.embeddings]

with Session(engine) as session:
    for chunk, embedding in zip(chunks, embedding):
        document_chunk = DocumentChunk(
            content=chunk.page_content,
            chunk_metadata=chunk.metadata,
            embedding=embedding
        )
        session.add(document_chunk)

    session.commit()