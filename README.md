# SHL Conversational Assessment Recommender

FastAPI service for SHL AI Intern assignment.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health:
```bash
curl http://127.0.0.1:8000/health
```

Chat:
```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Hiring a mid-level Java backend developer with Spring and SQL. Include personality."}]}'
```

## Catalog

Preferred: save the supplied SHL JSON as `data/catalog.json`.
If missing, the app attempts to download it from the assignment catalog URL using `CATALOG_URL` env var/default URL.

## Design

- Stateless POST `/chat`: full conversation history is sent every call.
- Catalog-only recommendations: output items are selected only from loaded catalog.
- Hybrid retrieval: word TF-IDF + character TF-IDF + domain boosts from public traces.
- Rule layer handles clarification, refinement, comparison, refusal.
- Exact schema: `{reply, recommendations, end_of_conversation}`.
