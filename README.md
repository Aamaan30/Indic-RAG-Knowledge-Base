# Indic-RAG Knowledge Base

A specialized semantic search engine and corpus-processing pipeline built to parse and index ancient Indian knowledge texts.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL with `pgvector`
- **ORM:** SQLAlchemy (Async)
- **AI Orchestration:** LangChain
- **Embeddings:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)
- **LLM Inference:** Groq API (`llama-3.1-8b-instant`)

## Getting Started

### Prerequisites
1. Ensure you have Docker and Docker Compose installed (if running via Docker).
2. Install Python 3.11+.

### Environment Setup
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Running Locally
To run the application natively on your machine:
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python manage.py run
```
The application and its academic frontend UI will be available at `http://localhost:8000/`.

### Running with Docker
```bash
docker-compose up --build
```
*(Note: To avoid conflicts with other projects, the Docker setup maps the FastAPI web server to port `8001` and the Postgres database to port `5433`)*

## Architecture
- **Batch Background Ingestion**: On startup, the application reads ancient texts from the `data/` directory, chunks them, computes vector embeddings, and stores them in PostgreSQL asynchronously.
- **Semantic Verse Finder**: Real-time semantic retrieval of specific verses based on meaning rather than exact keyword matches.
- **Deep Scholar AI Analysis**: Leverages Llama 3 to provide deep philosophical and academic breakdowns of the retrieved context.
