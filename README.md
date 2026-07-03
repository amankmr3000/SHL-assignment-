# SHL Conversational Assessment Recommender

This project was built as part of the **SHL Conversational Assessment
Recommendation Assignment**.

The chatbot recommends SHL assessments based on hiring requirements. It
can understand multi-turn conversations, ask follow-up questions when
the user's request is vague, update recommendations when requirements
change, compare SHL assessments, and refuse requests outside the scope
of SHL assessments.

------------------------------------------------------------------------

## Live Demo

**API**

https://shl-ai-xjeh.onrender.com

**Swagger UI**

https://shl-ai-xjeh.onrender.com/docs

**ReDoc**

https://shl-ai-xjeh.onrender.com/redoc

------------------------------------------------------------------------

## Features

-   Built using FastAPI
-   Stateless conversation handling
-   SHL catalog-based recommendations
-   Clarifies vague hiring requests
-   Supports recommendation refinement
-   Compares SHL assessments
-   Rejects prompt injection and unrelated requests
-   Returns only official SHL assessment URLs
-   Deployed on Render
-   Automated test suite (32 tests)

------------------------------------------------------------------------

## Tech Stack

-   Python
-   FastAPI
-   Pydantic
-   scikit-learn
-   NumPy
-   Uvicorn
-   Render

------------------------------------------------------------------------

## Running Locally

``` bash
git clone https://github.com/amankmr3000/SHL-assignment-.git
cd SHL-assignment-
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## Running Tests

``` bash
python -m pytest
```

**Current Status:** 32 / 32 tests passing

------------------------------------------------------------------------

## What I Learned

-   FastAPI backend development
-   REST API design
-   Stateless conversational systems
-   TF-IDF-based retrieval
-   Recommendation ranking
-   Backend testing with pytest
-   Deploying Python applications on Render

------------------------------------------------------------------------

## Future Improvements

-   Embedding-based semantic retrieval
-   Vector search (FAISS)
-   Docker support
-   GitHub Actions
-   Frontend chat interface

------------------------------------------------------------------------

## Repository

https://github.com/amankmr3000/SHL-assignment-

------------------------------------------------------------------------

## Author

**Aman Kumar**

Built for the SHL Conversational Assessment Recommendation Assignment.
