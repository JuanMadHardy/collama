# 📘 **Manual Completo: LangChain + Ollama + ChromaDB**
### *Documentación oficial para desarrolladores junior y mid-level*

---

# 1. Introducción

Este manual describe cómo construir aplicaciones de IA **locales, privadas y escalables** utilizando:

- **LangChain** → Framework para orquestación de LLMs
- **Ollama** → Servidor local de modelos
- **ChromaDB** → Base vectorial local para RAG

El objetivo es que cualquier desarrollador del equipo pueda:

- Entender la arquitectura
- Crear pipelines de RAG
- Construir agentes
- Mantener proyectos reales en producción local

---

# 2. Arquitectura General

```
                ┌──────────────────────────┐
                │        Usuario           │
                └─────────────┬────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   LangChain     │
                    │  (Orquestación) │
                    └───────┬─────────┘
                            │
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                    ▼
┌──────────────┐   ┌────────────────┐   ┌──────────────────┐
│ Prompting    │   │  Ollama LLM    │   │   ChromaDB        │
│ Templates    │   │ (Inferencia)   │   │ (Vector Store)    │
└──────────────┘   └────────────────┘   └──────────────────┘
```

---

# 3. Instalación y Configuración

## 3.1 Requisitos

- Ubuntu 25
- Python 3.10+
- 8GB RAM mínimo
- GPU opcional (recomendado)

## 3.2 Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3.3 Instalar LangChain

```bash
pip install langchain langchain-community langchain-ollama
```

## 3.4 Instalar Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verificar:

```bash
ollama list
```

## 3.5 Instalar ChromaDB

```bash
pip install chromadb
```

---

# 4. Primeros Pasos

## 4.1 Tu primer LLM local

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral")
print(llm.invoke("Hola, ¿qué puedes hacer?"))
```

## 4.2 Primer Prompt Template

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente técnico."),
    ("user", "{pregunta}")
])
```

## 4.3 Primera Chain

```python
chain = prompt | llm
print(chain.invoke({"pregunta": "Explica qué es LangChain"}))
```

---

# 5. Document Loaders

LangChain soporta loaders para:

- PDF
- Markdown
- HTML
- DOCX
- TXT

Ejemplo:

```python
from langchain.document_loaders import TextLoader

docs = TextLoader("manual.txt").load()
```

---

# 6. Chunking y Preprocesado

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)
```

---

# 7. Embeddings Locales con Ollama

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="mistral")
```

---

# 8. ChromaDB en Profundidad

## 8.1 Crear base vectorial

```python
from langchain.vectorstores import Chroma

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="db"
)
```

## 8.2 Recuperación

```python
retriever = db.as_retriever()
result = retriever.get_relevant_documents("¿Cómo configuro el sistema?")
```

---

# 9. Construcción de un RAG Completo

```python
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=ChatOllama(model="mistral"),
    retriever=retriever,
    chain_type="stuff"
)

print(qa.invoke("Explica el contenido del manual"))
```

---

# 10. Agentes y Herramientas

## 10.1 Crear herramienta personalizada

```python
from langchain.tools import tool

@tool
def contar_palabras(texto: str) -> int:
    return len(texto.split())
```

## 10.2 Crear agente

```python
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=[contar_palabras],
    llm=ChatOllama(model="mistral"),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

agent.invoke("Cuenta las palabras de: Hola mundo desde LangChain")
```

---

# 11. Patrones de Diseño Recomendados

- Separar prompts en `/prompts`
- Separar chains en `/chains`
- Separar agentes en `/agents`
- Mantener loaders en `/loaders`
- Persistir ChromaDB en `/db`
- Versionar modelos Ollama

---

# 12. Seguridad y Privacidad

- No mezclar datos sensibles en prompts
- No registrar contenido confidencial
- Usar entornos aislados
- Mantener control de acceso a la carpeta `/db`

---

# 13. Errores Comunes

| Error | Causa | Solución |
|------|--------|----------|
| Ollama no arranca | Servicio detenido | `systemctl restart ollama` |
| Chroma no persiste | Falta `persist_directory` | Añadir parámetro |
| RAG devuelve basura | Chunking incorrecto | Ajustar tamaño |
| Agente entra en loop | Herramientas mal definidas | Añadir límites |

---

# 14. Plantillas de Proyecto

```
project/
│
├── agents/
├── chains/
├── data/
├── db/
├── loaders/
├── prompts/
├── rag/
└── main.py
```

---

# 15. Apéndices

## 15.1 Glosario

- **LLM**: Large Language Model
- **RAG**: Retrieval-Augmented Generation
- **Embedding**: Vector numérico que representa texto
- **Vector Store**: Base de datos para embeddings

## 15.2 Cheatsheet

- `ChatOllama` → LLM local
- `OllamaEmbeddings` → Embeddings locales
- `Chroma` → Vector store
- `RetrievalQA` → RAG listo para usar

---