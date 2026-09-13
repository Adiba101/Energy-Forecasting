"""
Lightweight RAG (Retrieval-Augmented Generation) Engine
Indexes local energy knowledge documents and retrieves relevant snippets.
Uses a pure-Python TF-IDF / BM25 lexical retriever with zero external heavy dependencies.
"""

import os
import re
import math
from typing import List, Dict, Any

class KnowledgeRetriever:
    def __init__(self, knowledge_dir: str = "data/knowledge_base"):
        self.knowledge_dir = knowledge_dir
        self.chunks: List[Dict[str, Any]] = []
        self.vocabulary: Dict[str, int] = {}
        self.doc_freq: Dict[str, int] = {}
        self.total_docs: int = 0
        self.avg_doc_len: float = 0.0
        self.load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer: lowercase, strip punctuation, word tokens >= 2 chars."""
        words = re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', text.lower())
        # Filter basic stop words
        stopwords = {
            'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'in', 'to', 'for', 'of',
            'with', 'by', 'as', 'this', 'that', 'it', 'from', 'be', 'are', 'was', 'were',
            'or', 'not', 'your', 'you', 'our', 'can', 'will', 'have', 'has', 'had'
        }
        return [w for w in words if w not in stopwords]

    def load_and_index(self):
        """Loads text files from the knowledge directory and builds BM25 index."""
        self.chunks = []
        if not os.path.exists(self.knowledge_dir):
            return

        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(('.txt', '.md')):
                filepath = os.path.join(self.knowledge_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    continue

                # Split by sections / double newlines
                sections = re.split(r'\n(?=## |\n)', content)
                for sec_idx, section in enumerate(sections):
                    cleaned_section = section.strip()
                    if len(cleaned_section) < 40:
                        continue
                    tokens = self._tokenize(cleaned_section)
                    if tokens:
                        self.chunks.append({
                            "id": f"{filename}#sec{sec_idx}",
                            "source": filename,
                            "text": cleaned_section,
                            "tokens": tokens,
                            "len": len(tokens)
                        })

        self.total_docs = len(self.chunks)
        if self.total_docs == 0:
            return

        # Calculate Document Frequencies (DF)
        self.doc_freq = {}
        total_len = 0
        for chunk in self.chunks:
            unique_tokens = set(chunk["tokens"])
            total_len += chunk["len"]
            for token in unique_tokens:
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1

        self.avg_doc_len = total_len / self.total_docs

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the top-k most relevant chunks using BM25 scoring algorithm.
        BM25 parameters: k1=1.5, b=0.75
        """
        if not self.chunks or not query:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        k1 = 1.5
        b = 0.75
        scores = []

        for chunk in self.chunks:
            score = 0.0
            chunk_tokens = chunk["tokens"]
            chunk_len = chunk["len"]
            
            # Count term occurrences in this chunk
            term_counts = {}
            for t in chunk_tokens:
                term_counts[t] = term_counts.get(t, 0) + 1

            for q_token in query_tokens:
                if q_token in term_counts:
                    tf = term_counts[q_token]
                    df = self.doc_freq.get(q_token, 0)
                    
                    # IDF with Robertson-Spärck Jones smoothing
                    idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1.0)
                    
                    # BM25 TF component
                    tf_component = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (chunk_len / (self.avg_doc_len or 1.0))))
                    score += idf * tf_component

            if score > 0:
                scores.append((score, chunk))

        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)
        top_results = []
        for score, chunk in scores[:top_k]:
            top_results.append({
                "score": round(score, 3),
                "source": chunk["source"],
                "text": chunk["text"],
                "snippet": chunk["text"][:280] + ("..." if len(chunk["text"]) > 280 else "")
            })

        return top_results

    def format_context_block(self, results: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks into a clean prompt context block."""
        if not results:
            return "No specific energy knowledge documents retrieved for this query."
            
        formatted = ["### Verified Knowledge Context:"]
        for idx, item in enumerate(results, 1):
            formatted.append(f"[{idx}] (Source: {item['source']})")
            formatted.append(item['text'])
            formatted.append("---")
        return "\n".join(formatted)


# Global retriever instance
_retriever_instance = None

def get_knowledge_retriever() -> KnowledgeRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = KnowledgeRetriever()
    return _retriever_instance
