# SHL Conversational Assessment Recommender – Approach

## 1. Overview

The goal of this project was to build a conversational chatbot that recommends SHL assessments based on the user's hiring requirements. The chatbot follows the assignment requirements by exposing two FastAPI endpoints:

- **GET /health** – checks whether the service is running.
- **POST /chat** – accepts the complete conversation history and returns the next reply along with assessment recommendations whenever enough information is available.

The chatbot is completely stateless, so it does not store any conversation information on the server.

## 2. Overall Design

I divided the project into a few simple modules:

- **main.py** handles the API endpoints.
- **agent.py** contains the conversation logic.
- **retriever.py** searches and ranks assessments from the SHL catalog.
- **catalog.py** loads the catalog data.
- **models.py** defines the request and response schemas.

This separation made the code easier to understand, test, and modify.

## 3. Retrieval Approach

The SHL catalog is converted into a JSON file containing assessment names, URLs, descriptions, job levels, languages, durations, and categories.

To retrieve relevant assessments, I combined three ideas:

- Word-level TF-IDF similarity
- Character-level TF-IDF similarity
- Rule-based boosting for common job roles

TF-IDF helps match the user's query with assessment descriptions. Character-level matching improves results for abbreviations or partial names like "OPQ", "AWS", or "GSA".

I noticed that using only TF-IDF often returned generic assessments before role-specific ones. To improve this, I added role-based boosting and promotion for common hiring scenarios such as Java Backend, Finance, Customer Service, Administration, and Leadership.

## 4. Conversation Handling

The chatbot supports the four required behaviors.

### Clarification

If the user gives a vague request such as:

> I need an assessment

the chatbot asks follow-up questions instead of recommending immediately.

### Recommendation

Once enough information is available, the chatbot returns between one and ten SHL assessments.

Every recommendation includes:

- assessment name
- official SHL URL
- assessment type

### Refinement

The chatbot understands follow-up changes.

For example:

> Actually remove personality tests.

Instead of starting over, it updates the shortlist by removing personality assessments while keeping the earlier role context.

### Comparison

If the user asks to compare two assessments, the chatbot retrieves both assessments from the catalog and compares them using catalog descriptions instead of relying on model memory.

## 5. Safety and Scope Control

The chatbot only discusses SHL assessments.

It refuses:

- legal advice
- general hiring advice outside the assessment scope
- prompt injection attempts
- unrelated topics

This helps keep the system aligned with the assignment and prevents non-catalog recommendations.

## 6. Testing

I created automated tests to verify the required behaviors.

The tests cover:

- health endpoint
- schema compliance
- vague query clarification
- recommendation generation
- refinement
- assessment comparison
- prompt injection refusal
- legal/off-topic refusal
- edge cases
- stress cases

At the time of submission, all **32 tests were passing** locally.

## 7. Deployment

The project is deployed on Render.

Main technologies used:

- Python
- FastAPI
- Pydantic
- scikit-learn
- NumPy
- Uvicorn
- Render

Live API:

https://shl-ai-xjeh.onrender.com

GitHub repository:

https://github.com/amankmr3000/SHL-assignment-

## 8. What Did Not Work Initially

Initially, I used only TF-IDF similarity for ranking assessments. It worked for simple queries but sometimes ranked generic or repeated assessments above more useful role-specific ones.

For example, Java backend queries sometimes returned too many SQL-related assessments. I improved this by adding:

- role-specific promotion
- diversity filtering
- refinement-aware exclusions
- exact catalog matching for known assessments

These changes gave more stable and relevant recommendations during testing.

## 9. Future Improvements

If I continue improving the project, I would add:

- embedding-based semantic retrieval
- FAISS or Chroma for vector search
- a larger evaluation set for Recall@10
- better support for uncommon job roles
- a simple web UI for demo purposes

## Conclusion

This project satisfies the assignment requirements by providing a stateless conversational recommendation API grounded in the SHL catalog. It clarifies vague requests, recommends catalog assessments, handles refinements, compares assessments, refuses out-of-scope requests, and is deployed as a live FastAPI service.
