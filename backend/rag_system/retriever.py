# ================================================
# retriever.py — RAG Retriever
# ================================================
# YE FILE KYA KARTI HAI?
# 1. Query se similar documents dhundti hai
# 2. Context banati hai
# 3. Groq se answer generate karti hai
# ================================================

from rag_system.vectorstore import search_similar
from agents.career_agent import client
from config import settings
from typing import List


def retrieve_and_generate(
    query: str,
    top_k: int = 3
) -> str:
    """
    RAG Pipeline:
    1. Similar docs retrieve karo
    2. Context banao
    3. Groq se answer generate karo
    """

    # Step 1: Similar documents dhundo
    results = search_similar(query, top_k=top_k)

    if not results:
        return (
            "Knowledge base mein relevant "
            "information nahi mili!"
        )

    # Step 2: Context banao
    context_parts = []
    for i, result in enumerate(results, 1):
        context_parts.append(
            f"Source {i}:\n{result['document'][:400]}"
        )

    context = "\n\n".join(context_parts)

    # Step 3: Groq se answer generate karo
    prompt = f"""You are an expert AI Career Mentor for Indian tech students.

Use the following context to answer the question accurately.

Context:
{context}

Question: {query}

Instructions:
- Answer in English
- Be specific and actionable
- Focus on Indian job market
- Keep answer concise but complete
- Be encouraging and motivating"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Generation error: {e}")
        return f"Retrieved: {results[0]['document'][:300]}..."


def search_knowledge(
    query: str,
    top_k: int = 3
) -> List[str]:
    """Sirf documents retrieve karo"""
    results = search_similar(query, top_k=top_k)
    return [r["document"] for r in results]