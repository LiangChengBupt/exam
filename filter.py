from abc import ABC, abstractmethod
from typing import List, Dict
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FilterStrategy(ABC):
    @abstractmethod
    def filter(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        pass

class RuleBasedFilterStrategy(FilterStrategy):
    def __init__(self, keywords: List[str], threshold: float = 0.5):
        self.keywords = keywords
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer()
        self.keyword_vector = self.vectorizer.fit_transform(self.keywords)
        self.hash_set = set()

    def _hash_content(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _is_relevant(self, content: str) -> bool:
        if not self.keywords:
            return True
        content_vector = self.vectorizer.transform([content])
        similarity = cosine_similarity(content_vector, self.keyword_vector).flatten()
        return max(similarity) > self.threshold

    def filter(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        filtered_items = []
        for item in items:
            content_hash = self._hash_content(item['content'])
            if content_hash not in self.hash_set :
                self.hash_set.add(content_hash)
                filtered_items.append(item)
        return filtered_items

class ModelBasedFilterStrategy(FilterStrategy):
    def __init__(self, model, threshold: float = 0.5):
        self.model = model
        self.threshold = threshold
        self.hash_set = set()

    def _hash_content(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _is_relevant(self, content: str) -> bool:
        prediction = self.model.predict([content])
        return prediction[0] > self.threshold

    def filter(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        filtered_items = []
        for item in items:
            content_hash = self._hash_content(item['content'])
            if content_hash not in self.hash_set and self._is_relevant(item['content']):
                self.hash_set.add(content_hash)
                filtered_items.append(item)
        return filtered_items

class ContentFilter:
    def __init__(self, strategy: FilterStrategy):
        self.strategy = strategy

    def filter(self, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return self.strategy.filter(items)

import json
def main():
    with open('baidu/url_contents.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    # 选择筛选策略
    strategy = RuleBasedFilterStrategy(keywords=['清华大学', '研究', '论文'])
    content_filter = ContentFilter(strategy=strategy)

    filtered_items = content_filter.filter(items)

    with open('filtered_contents.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_items, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
