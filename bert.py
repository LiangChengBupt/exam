from sentence_transformers import SentenceTransformer, util

# 加载预训练的 Sentence-BERT 模型
model = SentenceTransformer('bert-base-nli-mean-tokens')

# 定义两段要比较的话
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast, dark-colored fox leaps over a sleepy dog."

# 获取每段话的嵌入表示
embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)

# 计算余弦相似度
similarity = util.pytorch_cos_sim(embedding1, embedding2)

print(f"Similarity between the two sentences: {similarity.item()}")