#!/usr/bin/env python3
"""
Lightweight Vector Indexing Tool
轻量化向量索引工具 - 用于对知识分片执行毫秒级检索
使用简单的 TF-IDF + Cosine Similarity 实现（无需安装重型向量库）
"""

import json
import os
from pathlib import Path
from math import log, sqrt
from collections import Counter

class SimpleVectorStore:
    def __init__(self, shards_dir):
        self.shards_dir = Path(shards_dir)
        self.index_file = self.shards_dir / "vector_index.json"
        self.shards = []
        self.vocab = {}
        self.vectors = []

    def _tokenize(self, text):
        # 极简分词：小写化并提取字母数字字符
        import re
        return re.findall(r'\w+', text.lower())

    def build_index(self):
        """扫描所有分片并建立 TF-IDF 索引"""
        print(f"🔍 正在从 {self.shards_dir} 构建向量索引...")
        
        all_shards = list(self.shards_dir.glob("**/*.md")) + list(self.shards_dir.glob("**/*.json"))
        if not all_shards:
            print("⚠️ 未发现可分片文件。")
            return

        documents = []
        for p in all_shards:
            try:
                content = p.read_text(encoding='utf-8')
                documents.append({"path": str(p), "content": content})
            except:
                continue

        # 计算 TF-IDF
        num_docs = len(documents)
        df = Counter()
        doc_tfs = []

        for doc in documents:
            tokens = self._tokenize(doc['content'])
            tf = Counter(tokens)
            doc_tfs.append(tf)
            for word in tf:
                df[word] += 1

        # 构建词汇表和向量
        self.vocab = {word: i for i, word in enumerate(df)}
        self.vectors = []
        
        for doc_idx, tf in enumerate(doc_tfs):
            vector = {}
            for word, count in tf.items():
                idf = log(num_docs / (df[word] + 1))
                vector[self.vocab[word]] = count * idf
            self.vectors.append({"path": documents[doc_idx]['path'], "vector": vector})

        # 持久化
        self.save()
        print(f"✅ 索引构建完成，共处理 {num_docs} 个文档。")

    def save(self):
        data = {
            "vocab": self.vocab,
            "vectors": self.vectors
        }
        self.index_file.write_text(json.dumps(data, indent=2))

    def load(self):
        if not self.index_file.exists():
            self.build_index()
        data = json.loads(self.index_file.read_text())
        self.vocab = data['vocab']
        self.vectors = data['vectors']

    def search(self, query, top_k=3):
        """对比余弦相似度进行内容检索"""
        if not self.vocab:
            self.load()

        query_tokens = self._tokenize(query)
        query_tf = Counter(query_tokens)
        query_vec = {}
        
        for word, count in query_tf.items():
            if word in self.vocab:
                query_vec[self.vocab[word]] = count

        results = []
        for doc in self.vectors:
            score = self._cosine_similarity(query_vec, doc['vector'])
            if score > 0:
                results.append({"path": doc['path'], "score": score})

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([val**2 for val in vec1.values()])
        sum2 = sum([val**2 for val in vec2.values()])
        denominator = sqrt(sum1) * sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

if __name__ == "__main__":
    # 默认针对知识分片目录
    store = SimpleVectorStore("【知识分片】(文档析构专家)")
    store.build_index()
    # 示例搜索
    # print(store.search("交易策略"))
