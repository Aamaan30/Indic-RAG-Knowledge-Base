import os

from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models.corpus import Corpus

embeddings_model = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("HF_TOKEN"),
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGroq(
    temperature=0.2,
    model_name="llama-3.1-8b-instant",
    groq_api_key=settings.GROQ_API_KEY
)

prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template="""You are an expert scholar of ancient Indian knowledge texts. 
Based on the provided textual context (verses), provide an educational and philosophical breakdown 
of the text in relation to the query.

Context:
{context}

Query:
{query}

Analysis:"""
)

chain = prompt_template | llm | StrOutputParser()


async def search_verses(query: str, db: AsyncSession, limit: int = 3):
    query_vector = embeddings_model.embed_query(query)

    # We use cosine distance.
    # To calculate similarity score from cosine distance: 1 - distance
    stmt = select(Corpus, Corpus.embedding.cosine_distance(query_vector).label('distance')) \
        .order_by(Corpus.embedding.cosine_distance(query_vector)) \
        .limit(limit)

    result = await db.execute(stmt)
    rows = result.all()

    results = []
    for row in rows:
        corpus = row.Corpus
        distance = row.distance
        similarity = 1.0 - distance
        results.append({
            "chapter": corpus.chapter,
            "verse_num": corpus.verse_num,
            "text": corpus.text,
            "similarity_score": similarity
        })

    return results


async def explain_query(query: str, db: AsyncSession):
    # 1. Get relevant context
    search_results = await search_verses(query, db, limit=5)

    if not search_results:
        return {"explanation": "No relevant verses found in the knowledge base.", "sources": []}

    # 2. Format context
    context_lines = []
    for res in search_results:
        loc = f"Chapter {res['chapter']}"
        if res['verse_num']:
            loc += f", Verse {res['verse_num']}"
        context_lines.append(f"[{loc}]: {res['text']}")

    context = "\n".join(context_lines)

    # 3. Generate explanation
    explanation = await chain.ainvoke({"context": context, "query": query})

    return {
        "explanation": explanation,
        "sources": search_results
    }
