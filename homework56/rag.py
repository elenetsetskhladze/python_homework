from dotenv import load_dotenv


load_dotenv()

from sqlalchemy import select
from sqlalchemy.orm import Session
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from database import engine
from models import DocumentChunk



client = genai.Client()

EMBEDDING_MODEL = "gemini-embedding-001"

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite",)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Answer the question based only
            on the following context.
            Don't add anything else, just answer the question.
            If you don't know the answer, just say that you don't know.
            """,
        ),
        ("human", "Context: {context}\n\nQuestion: {question}"),
    ]
)

def retrieve_documents(question: str):
    query_result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
    )

    query_embedding = query_result.embeddings[0].values

    query = (select(DocumentChunk).order_by(DocumentChunk.embedding.cosine_distance(query_embedding))).limit(3)

    with Session(engine) as session:
        results = session.execute(query).scalars().all()

    return results

def format_documents(documents):
    return "\n\n".join(chunk.content for chunk in documents)

def answer_question(question: str):
    documents = retrieve_documents(question)
    context = format_documents(documents)

    chain = prompt | llm | StrOutputParser()

    return chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )


while True:
    question = input("Enter your question (or 'exit' to quit): ")

    if question.lower() == "exit":
        break

    response = answer_question(question)

    print(response)




