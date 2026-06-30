# AI Question Generator API

A FastAPI backend that generates multiple-choice questions on a given topic using an AI model via OpenRouter, and stores them in a PostgreSQL database for retrieval.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL (via SQLAlchemy ORM)
- **AI Provider:** OpenRouter (model selectable per request)
- **Language:** Python 3.12

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── ai_routes.py          # POST /ai/generate
│   │   └── questions_routes.py   # GET /questions/
│   ├── database/
│   │   ├── db.py                 # SQLAlchemy engine + Base
│   │   └── session.py            # DB session dependency
│   ├── models/
│   │   └── question.py           # Question table schema
│   ├── schemas/
│   │   └── question_schema.py    # Pydantic enums (Topic, Difficulty)
│   └── services/
│       ├── ollama_service.py     # Calls OpenRouter, parses AI response
│       └── question_service.py   # Saves questions to DB
├── main.py                       # App entrypoint
├── requirements.txt
└── .env                          # DATABASE_URL, OPENROUTER_API_KEY (not committed)
```

## Setup & Running Locally

1. **Clone the repo and navigate into backend**

```bash
   git clone <your-repo-url>
   cd backend
```

2. **Create and activate a virtual environment**

```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
```

3. **Install dependencies**

```bash
   pip install -r requirements.txt
```

4. **Create a `.env` file** in `backend/` with:

```
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   OPENROUTER_API_KEY=<your_openrouter_api_key>
```

5. **Make sure PostgreSQL is running** and the database in `DATABASE_URL` exists. The `question` table is created automatically on startup.

6. **Run the server**

```bash
   uvicorn main:app --reload
```

7. **Open API docs** at `http://127.0.0.1:8000/docs` to test endpoints interactively.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/ai/generate` | Generate MCQs for a topic and save them |
| GET    | `/questions/` | Retrieve all saved questions |
| GET    | `/questions/{question_id}` | Retrieve a single question by ID |

## Project Flow

1. Client sends a request to `POST /ai/generate` with `topic`, `difficulty`, `count`, and `model`.
2. `ai_routes.py` receives the request and calls `ollama_service.generate_questions()`.
3. `ollama_service.py` builds a prompt and sends it to OpenRouter's chat completion API.
4. The AI's raw response is cleaned (strips markdown fences, extracts JSON array, validates parsing) and converted into a list of question objects.
5. `ai_routes.py` passes the parsed questions to `question_service.save_questions()`.
6. `question_service.py` maps each question into a `Question` ORM model and commits it to PostgreSQL.
7. The generated questions are returned to the client as the API response.
8. Separately, `GET /questions/` can be called at any time to retrieve all saved questions from the database via `questions_routes.py`.

## Flowchart

```mermaid
flowchart TD

    Client([Client / Swagger UI])

    Route1[POST /ai/generate<br/>ai_routes.py]
    Route2[GET /questions/<br/>questions_routes.py]

    AIService[ollama_service.py<br/>Build prompt, call OpenRouter]
    OpenRouter[(OpenRouter API)]
    Clean[Clean and parse JSON response]

    SaveService[question_service.py<br/>save_questions]
    DB[(PostgreSQL question table)]

    Client -->|topic, difficulty, count, model| Route1
    Route1 --> AIService
    AIService --> OpenRouter
    OpenRouter --> AIService
    AIService --> Clean
    Clean --> Route1
    Route1 --> SaveService
    SaveService --> DB
    Route1 -->|return generated questions| Client

    Client -->|fetch saved questions| Route2
    Route2 --> DB
    DB --> Route2
    Route2 -->|return question list| Client
```
## Prerequisites

Before running this project, make sure you have:

- **Python 3.12** installed (`python --version` to check)
- **PostgreSQL** installed and running, with a database created for this project
- **pip** (comes bundled with Python)
- **Git** (to clone the repository)
- An **OpenRouter API key** (see setup steps below)

## Setting up an OpenRouter Account

This project uses [OpenRouter](https://openrouter.ai) to access AI models for question generation.

1. Go to [openrouter.ai](https://openrouter.ai) and sign up using Google, GitHub, or email.
2. Navigate to **Keys** in the dashboard and create a new API key.
3. Add credits to your account if needed — OpenRouter is pay-as-you-go, and some models offer free-tier usage while others (e.g. `openai/gpt-4o-mini`) are billed per token.
4. Copy your API key and add it to the `.env` file as:
```
   OPENROUTER_API_KEY=your_key_here
```
5. Browse available models and pricing at [openrouter.ai/models](https://openrouter.ai/models). You can pass any supported model name in the `model` field when calling `/ai/generate`.

## Setting up Ollama (optional, for local AI inference)

> Note: this project currently uses OpenRouter by default. Ollama setup is only needed if you want to run AI inference locally instead of via OpenRouter.

1. Download and install Ollama from [ollama.com](https://ollama.com) for your OS.
2. Once installed, Ollama runs automatically as a background service.
3. Pull a model:
```bash
   ollama pull llama3
```
4. Verify the model is available:
```bash
   ollama list
```
5. Ollama serves locally at `http://localhost:11434` by default — no internet connection or API key required once the model is downloaded.

## Clone, Build & Run

```bash
# Clone the repository
git clone https://github.com/PRADEEP1625/AI-Question-Generator.git
cd AI-Question-Generator/backend

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create a .env file in backend/ with:
# DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
# OPENROUTER_API_KEY=<your_openrouter_api_key>

# Run the server
uvicorn main:app --reload
```

Once running, open `http://127.0.0.1:8000/docs` to test the API endpoints interactively. The `question` table is created automatically in PostgreSQL on first startup.
