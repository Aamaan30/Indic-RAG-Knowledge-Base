import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from api.endpoints import router
from core.db import engine, Base, AsyncSessionLocal
from services.parser import ingest_data_folder
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup: Create tables and enable vector extension if not exists
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
    # Run batch ingestion in the background
    async def run_ingestion():
        async with AsyncSessionLocal() as session:
            await ingest_data_folder(session, "data")
            
    asyncio.create_task(run_ingestion())
    
    yield
    # On shutdown
    pass

app = FastAPI(
    title="Indic-RAG Knowledge Base API",
    description="Semantic search engine and corpus-processing pipeline for ancient Indian knowledge texts.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
