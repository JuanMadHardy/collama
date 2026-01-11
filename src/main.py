from click import prompt
from langchain_ollama import ChatOllama
import chromadb
import uuid

llm = ChatOllama(
    model="phi3:mini",
    temperature=0,
    # other params...
)

chroma_client = chromadb.PersistentClient("./chroma_db")

collection = chroma_client.get_or_create_collection(name="concontra")

with open("csv/concontrata.csv", "r", encoding="utf-8") as f:

    policies: list[str] = f.read().splitlines()

    collection.add(
        ids=[str(uuid.uuid4()) for _ in policies],
        documents=policies,
        metadatas=[{"line": line} for line in range(len(policies))],
    )

result = collection.query(
    query_texts=[
        "facilidades de pago",
        "pago online",
    ],
    n_results=5,
)

for i, res in enumerate(result["documents"]):
    prompt = "\n".join(res)


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant",
    },
    {
        "role": "user",
        "content": f"Que facilidades hay de pago online?, Use this as context for answering: {prompt}",
    },
]

ai_msg = llm.invoke(messages)

print(ai_msg)
