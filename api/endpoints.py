from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel

from core.db import get_db
from services.search_engine import search_verses, explain_query

router = APIRouter()

class ExplainRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    chapter: Optional[str] = None
    verse_num: Optional[str] = None
    text: str
    similarity_score: float

class ExplainResponse(BaseModel):
    explanation: str
    sources: List[SearchResult]

@router.get("/search", response_model=List[SearchResult])
async def search(q: str = Query(..., description="Semantic search query"), db: AsyncSession = Depends(get_db)):
    results = await search_verses(q, db)
    return results

@router.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest, db: AsyncSession = Depends(get_db)):
    result = await explain_query(request.query, db)
    return result
