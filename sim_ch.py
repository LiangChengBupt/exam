import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from abc import ABC, abstractmethod
from gpt4 import query_gpt
class SimilarityCalculator(ABC):
    @abstractmethod
    def calculate_similarity(self, str1: str, str2: str) -> float:
        pass

class BertCosineSimilarityCalculator(SimilarityCalculator):
    def __init__(self, model_name='bert-base-chinese'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)

    def get_sentence_embedding(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors='pt', truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :]
        return cls_embedding

    def calculate_similarity(self, str1: str, str2: str) -> float:
        embedding1 = self.get_sentence_embedding(str1)
        embedding2 = self.get_sentence_embedding(str2)
        similarity = cosine_similarity(embedding1.numpy(), embedding2.numpy())[0][0]
        return similarity


# 示例：其他相似性计算方法，例如调用大模型API
class GPT4api(SimilarityCalculator):
    def __init__(self):
        pass
    def inference(self, str1, str2):
        prompt = f"""
        Please judge the similarity between the following two sentences:
        Sentence 1: {str1}
        Sentence 2: {str2}
        return the similarity score directly, DO NOT EXPLAIN.
        """
        return 0.85

    def calculate_similarity(self, str1: str, str2: str) -> float:
        return self.inference(str1, str2)

# 工厂类用于创建相似性计算器
class SimilarityCalculatorFactory:
    @staticmethod
    def create_calculator(method: str, **kwargs) -> SimilarityCalculator:
        if method == 'bert_cosine':
            return BertCosineSimilarityCalculator(**kwargs)
        elif method == 'gpt-4':
            return GPT4api(**kwargs)
        else:
            raise ValueError(f"Unknown method: {method}")

# 使用示例
def main():
    # method = 'bert_cosine'  
    method = 'gpt-4'
    calculator = SimilarityCalculatorFactory.create_calculator(method)

    str1 = "骨折并发症博禾医生百度首页提示：本内容仅作参考，不能代替面诊，如有不适请尽快线下就医骨折并发症朱建强副主任医师普通外科北京小汤山医院骨折后导致的并发症有很多，分为早期并发症和晚期病发症。       骨折的早期并发症主要包括严重的休克、脂肪栓塞综合征、重要器官损伤，还有重要周围组织的损伤，比如神经血管，还有骨筋膜室综合征。       骨折常见的晚期并发症有坠积性的肺炎、褥疮、下肢静脉血栓、感染，还有骨化性的肌炎、创伤性的关节炎、关节的僵直、骨萎缩、骨缺血性的坏死，还有缺血性的肌挛缩等。       骨折一旦出现要及时到正规的医院去救治，避免这些并发症的出现对身体造成严重的危害。展开全文"
    str2 = "骨折并发症"
    similarity = calculator.calculate_similarity(str1, str2)
    print(f"相似度 ({method}): {similarity}")

if __name__ == "__main__":
    main()
