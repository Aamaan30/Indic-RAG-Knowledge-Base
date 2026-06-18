import os
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.corpus import Corpus
from langchain_huggingface import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

async def ingest_data_folder(db: AsyncSession, folder_path: str = "data"):
    """
    Reads files from the data folder, parses them, and inserts them into the database.
    Expects text files to be formatted as:
    Chapter 1
    1.1: This is verse 1.
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            lines = content.split('\n')
            current_chapter = "Unknown"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.lower().startswith("chapter"):
                    current_chapter = line
                    continue
                
                # Try to extract verse number, e.g., "1.1: Verse text"
                match = re.match(r"^([\d\.]+)\s*:\s*(.*)", line)
                if match:
                    verse_num = match.group(1)
                    text = match.group(2)
                else:
                    verse_num = None
                    text = line
                
                if text:
                    # Check if already exists
                    stmt = select(Corpus).where(Corpus.text == text)
                    result = await db.execute(stmt)
                    if result.scalar_one_or_none():
                        continue # Skip existing
                        
                    embedding = embeddings_model.embed_query(text)
                    db_verse = Corpus(
                        chapter=current_chapter,
                        verse_num=verse_num,
                        text=text,
                        embedding=embedding
                    )
                    db.add(db_verse)
                    
            await db.commit()
            print(f"Ingested {filename}")
