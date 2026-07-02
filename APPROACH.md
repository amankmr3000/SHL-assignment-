# Approach Document

## Design
The system is a stateless FastAPI service with two endpoints: `GET /health` and `POST /chat`. The `/chat` endpoint receives full conversation history, reconstructs user intent from all user turns, and returns a reply plus an optional structured recommendation shortlist.

## Retrieval Setup
The SHL catalog is normalized into assessment records containing name, URL, description, job levels, languages, duration, remote/adaptive flags, keys, and derived test type. Recommendations are produced only from this loaded catalog, preventing hallucinated URLs.

For speed and reliability, retrieval uses a hybrid lexical model: word-level TF-IDF for semantic-ish role/skill matching and character n-gram TF-IDF for robust matching of product names, acronyms, versions, and technologies. A small rule-based boost layer improves Recall@10 for repeated patterns observed in public traces such as Java backend, graduate hiring, leadership, contact center, finance, admin assistant, cognitive, personality, and situational judgement.

## Agent Logic
The agent has deterministic guards before retrieval:
1. Refuse prompt injection, off-topic, and legal/compliance advice.
2. Ask clarification when the query is too vague.
3. Compare assessments when comparison intent is detected.
4. Refine recommendations by applying latest constraints such as removing OPQ/personality or coding tests.
5. Recommend 1-10 catalog items when enough context exists.

## Evaluation
The system was tested against public traces and behavior probes: vague first turns should not recommend, refined constraints should update output, comparison should use catalog descriptions, and every recommendation URL must come from the catalog. The response model is enforced with Pydantic to maintain schema compliance.

## What Did Not Work
A fully LLM-driven agent was avoided because it increased latency, risked schema drift, and could hallucinate non-catalog URLs. Pure keyword search was also weaker for role descriptions, so character n-grams and domain boosts were added.

## AI Tool Usage
AI assistance was used to accelerate scaffolding, retrieval design, and documentation drafting. Core choices were kept simple and explainable for interview discussion.
