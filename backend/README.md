# Market Alignment Engine

A modular Python backend API that enables deterministic market-alignment analysis using the LinkedIn Job Postings Dataset and local Llama 3 integration.

## Architecture Overview

The system is built as a pipeline of independent modules:

1.  **Data Loader**: Loads and filters job postings from a CSV dataset.
2.  **Skill Engine**:
    *   **Extraction**: Deterministic, dictionary-based substring matching to find skills in text.
    *   **Demand Scoring**: Calculates the frequency of each skill across the filtered job descriptions.
3.  **Gap Engine**: Compares candidate skills against market demand to identify and rank missing skills.
4.  **Planner**: Integrates with a local Ollama instance running Llama 3 to generate a 30-day learning roadmap.
5.  **FastAPI App**: Orchestrates the pipeline and exposes a REST API.

## Deterministic Market Engine & Demand Scoring

The engine uses a hardcoded dictionary (`config.py`) to ensure consistency.

**Demand Score Formula:**
```
demand_score = (count of job descriptions containing skill) / (total filtered job descriptions)
```
Scores are rounded to 3 decimal places.

## Weighted Gap Ranking

Missing skills are identified by subtracting the candidate's skills from the market's demanded skills.
They are then ranked solely by their **Demand Score** in descending order. This ensures the candidate focuses on the most valuable skills first.

## Ollama Integration

The `planner.py` module sends a structured prompt to a local Ollama instance (`http://localhost:11434`) running the `llama3` model. It requests a 30-day study plan for the top 5 missing skills.

## API Usage

### Endpoint: `POST /analyze`

**Request Body:**
```json
{
    "role_name": "Machine Learning Engineer",
    "resume_text": "I have experience with Python and SQL..."
}
```

**Response:**
```json
{
    "top_demanded_skills": [{"skill": "python", "score": 0.9}, ...],
    "candidate_skills": ["python", "sql"],
    "missing_skills": [{"skill": "tensorflow", "score": 0.7}, ...],
    "roadmap": "Week 1: ..."
}
```

## How to Run

1.  **Prerequisites**:
    *   Python 3.9+
    *   [Ollama](https://ollama.com/) installed and running (`ollama run llama3`).
    *   `job_postings.csv` placed in the project root.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Backend**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
