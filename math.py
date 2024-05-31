import gensim.downloader as api
from numpy.linalg import norm
import numpy as np

# 加载预训练的 GloVe 模型
glove_vectors = api.load("glove-wiki-gigaword-50")

# 定义一个函数来计算句子的平均词向量
def sentence_embedding(sentence):
    words = sentence.lower().split()
    word_vectors = [glove_vectors[word] for word in words if word in glove_vectors]
    if not word_vectors:
        return np.zeros(50)
    return np.mean(word_vectors, axis=0)

# 定义两段要比较的话
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast, dark-colored fox leaps over a sleepy dog."

# 获取每段话的嵌入表示
embedding1 = sentence_embedding(sentence1)
embedding2 = sentence_embedding(sentence2)

# 计算余弦相似度
similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

print(f"Similarity between the two sentences: {similarity}")