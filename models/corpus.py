from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from core.db import Base

class Corpus(Base):
    __tablename__ = "corpus"

    id = Column(Integer, primary_key=True, index=True)
    chapter = Column(String, nullable=True)
    verse_num = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    # 384 is the embedding dimension for sentence-transformers/all-MiniLM-L6-v2
    embedding = Column(Vector(384))
