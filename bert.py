from transformers import AutoTokenizer, AutoModel
import torch
from abc import ABC, abstractmethod
from typing import List

class SimilarityCalculator(ABC):
    @abstractmethod
    def compute_similarity(self, embedding1, embedding2) -> float:
        pass

class CosineSimilarityCalculator(SimilarityCalculator):
    def compute_similarity(self, embedding1, embedding2) -> float:
        return torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=0).item()

class SentenceSimilarity:
    def __init__(self, model_name: str, similarity_calculator: SimilarityCalculator):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.similarity_calculator = similarity_calculator

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embeddings(self, sentences: List[str]):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings

    def compute_similarity(self, sentence1: str, sentence2: str) -> float:
        embeddings = self.get_embeddings([sentence1, sentence2])
        return self.similarity_calculator.compute_similarity(embeddings[0], embeddings[1])

# 示例用法
if __name__ == "__main__":
    model_name = 'hiiamsid/sentence_similarity_spanish_es'
    cosine_similarity_calculator = CosineSimilarityCalculator()
    similarity_calculator = SentenceSimilarity(model_name, cosine_similarity_calculator)

    sentence1 = 'Mi nombre es Siddhartha'
    sentence2 = 'Mis amigos me llamaron por mi nombre Siddhartha'

    similarity = similarity_calculator.compute_similarity(sentence1, sentence2)
    print(f"Cosine similarity: {similarity}")
