import re
from typing import Any, Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BOOST_RULES = {
    "java": ["core java", "spring", "sql", "automata", "verify", "opq"],
    "backend": ["core java", "spring", "sql", "amazon web services", "docker", "automata"],
    "full stack": ["core java", "spring", "angular", "sql", "automata front end", "docker", "aws"],
    "developer": ["automata", "core java", "python", "sql", "verify"],
    "rust": ["smart interview", "automata", "linux programming", "networking", "verify", "opq"],
    "network": ["networking", "linux"],
    "contact center": ["contact center", "customer service", "svar", "conversational multichat"],
    "customer service": ["customer service", "contact center", "svar"],
    "finance": ["financial accounting", "verify numerical", "basic statistics", "graduate scenarios", "opq"],
    "graduate": ["verify interactive g", "opq32r", "graduate scenarios", "basic statistics"],
    "sales": ["sales", "global skills assessment", "opq", "motivation"],
    "admin": ["microsoft excel", "microsoft word", "administrative", "business communications", "opq"],
    "assistant": ["microsoft excel", "microsoft word", "administrative", "business communications", "opq"],
    "leadership": ["opq32r", "opq universal competency", "opq leadership", "global skills"],
    "executive": ["opq32r", "opq universal competency", "opq leadership"],
    "personality": ["opq32r", "occupational personality", "motivation questionnaire"],
    "cognitive": ["verify interactive g", "verify numerical", "verify verbal", "verify inductive"],
    "situational": ["graduate scenarios", "situational judgement"],
}

class Retriever:
    def __init__(self, catalog: List[Dict[str, Any]]):
        self.catalog = catalog
        self.texts = [x["search_text"] for x in catalog]
        self.word_vec = TfidfVectorizer(ngram_range=(1,2), stop_words="english", min_df=1)
        self.char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3,5), min_df=1)
        self.word_mat = self.word_vec.fit_transform(self.texts)
        self.char_mat = self.char_vec.fit_transform(self.texts)

    def search(self, query: str, top_k: int = 10, include_personality: bool = True, exclude: List[str] | None = None) -> List[Dict[str, Any]]:
        q = query.lower()
        exclude = [e.lower() for e in (exclude or [])]
        sw = cosine_similarity(self.word_vec.transform([q]), self.word_mat)[0]
        sc = cosine_similarity(self.char_vec.transform([q]), self.char_mat)[0]
        boost = self._boost(q)
        scores = 0.6 * sw + 0.2 * sc + 1.4 * boost
        order = np.argsort(-scores)
        ans = []
        for idx in order:
            item = self.catalog[int(idx)]
            blob = (item["name"] + " " + item["search_text"]).lower()
            if any(e in blob for e in exclude): continue
            if not include_personality and ("P" in item.get("test_type", "") or "personality" in blob or "opq" in blob): continue
            ans.append(item)
            if len(ans) >= top_k: break
        return ans

    def find(self, text: str, n: int = 3) -> List[Dict[str, Any]]:
        return self.search(text, top_k=n, include_personality=True)

    def _boost(self, q: str) -> np.ndarray:
        b = np.zeros(len(self.catalog))
        for trigger, names in BOOST_RULES.items():
            if trigger in q:
                for i, item in enumerate(self.catalog):
                    nm = item["name"].lower()
                    blob = item["search_text"]
                    for rank, target in enumerate(names):
                        if target in nm or target in blob:
                            b[i] += max(3.0 - rank * 0.25, 0.8)
        return b
