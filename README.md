# SHL Conversational Assessment Recommender

This project was built as part of the **SHL Conversational Assessment
Recommendation Assignment**.

The chatbot recommends SHL assessments based on hiring requirements. It
understands multi-turn conversations, asks follow-up questions when
requests are vague, updates recommendations when requirements change,
compares SHL assessments, and refuses requests outside the scope of SHL
assessments.

------------------------------------------------------------------------

# Live Demo

### API

https://shl-ai-xjeh.onrender.com

### Swagger UI

https://shl-ai-xjeh.onrender.com/docs

### ReDoc

https://shl-ai-xjeh.onrender.com/redoc

------------------------------------------------------------------------

# Features

-   Stateless FastAPI backend
-   SHL catalog-based recommendations
-   Clarifies vague hiring requests
-   Supports recommendation refinement
-   Compares SHL assessments
-   Rejects prompt injection and unrelated requests
-   Returns only official SHL assessment URLs
-   Deployed on Render
-   32 automated tests

------------------------------------------------------------------------

# Project Structure

``` text
shl_fast/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── retriever.py
│   ├── catalog.py
│   └── models.py
│
├── data/
│   └── catalog.json
│
├── scripts/
│   └── download_catalog.py
│
├── tests/
│   ├── test_api.py
│   ├── test_behaviors.py
│   ├── test_final_behaviors.py
│   ├── test_edge_cases.py
│   └── test_stress_behaviors.py
│
├── APPROACH.md
├── README.md
├── Procfile
├── requirements.txt
└── runtime.txt
```

------------------------------------------------------------------------

# Tech Stack

-   Python
-   FastAPI
-   Pydantic
-   scikit-learn
-   NumPy
-   Uvicorn
-   Render

------------------------------------------------------------------------

# API Endpoints

  Method   Endpoint    Description
  -------- ----------- -----------------------------------
  GET      `/`         Service information
  GET      `/health`   Health check
  POST     `/chat`     Conversational recommendation API

------------------------------------------------------------------------

# Running Locally

``` bash
git clone https://github.com/amankmr3000/SHL-assignment-.git
cd SHL-assignment-
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# Running Tests

``` bash
python -m pytest
```

**Current Status:** 32 / 32 tests passing

------------------------------------------------------------------------

# What I Learned

-   FastAPI backend development
-   REST API design
-   Stateless conversational systems
-   TF-IDF based retrieval
-   Recommendation ranking
-   Backend testing using pytest
-   Deploying Python applications on Render

------------------------------------------------------------------------

# Future Improvements

-   Embedding-based semantic retrieval
-   Vector search (FAISS)
-   Docker support
-   GitHub Actions CI/CD
-   Simple frontend chat interface

------------------------------------------------------------------------

# Repository

https://github.com/amankmr3000/SHL-assignment-

------------------------------------------------------------------------

# Author

**Aman Kumar**

Built for the SHL Conversational Assessment Recommendation Assignment.
