from dotenv import load_dotenv

load_dotenv()

from google import genai
from sqlalchemy.orm import Session
from sqlalchemy import select
from langchain_google_genai import ChatGoogleGenerativeAI

from database import engine
from models import DocumentChunk

client = genai.Client()

question = input('Enter question: ')

query_result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)

query_embedding = query_result.embeddings[0].values

query = select(DocumentChunk).order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(3)

with Session(engine) as session:
    results = session.execute(query).scalars().all()



llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

context = "\n\n".join(result.content for result in results)

response = llm.invoke(
    f"""
    Answer the question based only on the following context:
    Context: {context}
    Question: {question}
    """
)

print(response.text)


