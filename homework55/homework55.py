from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from sklearn.metrics.pairwise import cosine_similarity

client = genai.Client()

loader = UnstructuredMarkdownLoader("hotel_info.md")

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40)

chunks = splitter.split_documents(docs)

texts = [chunk.page_content for chunk in chunks]

result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=texts
)

embedding = [item.values for item in result.embeddings]

question = "რომელ საათზე უნდა დავტოვო ნომერი?"

query_result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=question
)

embedding_query = query_result.embeddings[0].values

similarity_scores = cosine_similarity([embedding_query], embedding)[0]

result = sorted(zip(chunks, similarity_scores), key=lambda x: x[1], reverse=True)

for i, (chunk, score) in enumerate(result[:3], start=1):
    print(f"chunk {i+1}:")
    print(f"Score: {score}")
    print(f"Data: {chunk.page_content}")