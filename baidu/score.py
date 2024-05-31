import sacrebleu
from datasets import load_metric
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from gpt4 import query_gpt
from bert_score import score
from keyword import zh_medical_words
# 示例文章
# article1 = "骨折并发症"
# article2 = "骨折并发症博禾医生百度首页提示：本内容仅作参考，不能代替面诊，如有不适请尽快线下就医骨折并发症朱建强副主任医师普通外科北京小汤山医院骨折后导致的并发症有很多，分为早期并发症和晚期病发症。       骨折的早期并发症主要包括严重的休克、脂肪栓塞综合征、重要器官损伤，还有重要周围组织的损伤，比如神经血管，还有骨筋膜室综合征。       骨折常见的晚期并发症有坠积性的肺炎、褥疮、下肢静脉血栓、感染，还有骨化性的肌炎、创伤性的关节炎、关节的僵直、骨萎缩、骨缺血性的坏死，还有缺血性的肌挛缩等。       骨折一旦出现要及时到正规的医院去救治，避免这些并发症的出现对身体造成严重的危害。展开全文"

# BLEU Score
def calculate_bleu(reference, hypothesis):
    bleu = sacrebleu.corpus_bleu([hypothesis], [[reference]])
    return bleu.score

# GLUE Score (MNLI)
def calculate_glue(reference, hypothesis):
    tokenizer = AutoTokenizer.from_pretrained('textattack/bert-base-uncased-MNLI')
    model = AutoModelForSequenceClassification.from_pretrained('textattack/bert-base-uncased-MNLI')
    inputs = tokenizer(reference, hypothesis, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)
    return probabilities.numpy()

def calculate_gpt4(self,query , content):
    prompt = f"""
    I want to judge whether the content is related to the search query.
    Search query: {query}
    Content: {content}
    Please respond with the True/False directly, DO NOT EXPLAIN.
    """
    return query_gpt(prompt)=='True'

# BERTScore
def calculate_bertscore(reference, hypothesis):
    P, R, F1 = score([hypothesis], [reference], lang='en', model_type='bert-base-uncased')
    return P.mean().item(),R.mean().item(),F1.mean().item()


def rule_based_filter(content):
    """
    Use keyword matching to filter out medical-related samples from parquet files
    """
    match_count = 0
    threshold = 5
    for keyword in zh_medical_words:
        if keyword in content:
            match_count += 1
    if match_count > threshold:
        return True
    else:
        return False
# print(article1)
# print(article2)
# # 计算相似度分数
# bleu_score = calculate_bleu(article1, article2)
# glue_scores = calculate_glue(article1, article2)
# bertscore = calculate_bertscore(article1, article2)

# print(f"BLEU Score: {bleu_score}")
# print(f"GLUE Scores: {glue_scores}")
# print(f"BERTScore: {bertscore}")

