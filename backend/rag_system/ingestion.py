# ================================================
# ingestion.py — Knowledge Base Ingestion
# ================================================
# EK BAAR RUN KARO:
# python rag_system/ingestion.py
# ================================================

import sys
import os
sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from rag_system.vectorstore import create_vector_store

CAREER_DOCUMENTS = [
    """Software Engineering Career Path in India 2024:
    Essential Skills: Python, JavaScript, Data Structures,
    Algorithms, Git, SQL, REST APIs.
    Important Skills: React, Node.js, Docker, AWS, System Design.
    Salary: Fresher 4-8 LPA, 1-2 years 8-15 LPA, 3-5 years 15-30 LPA.
    Top Companies: TCS, Infosys, Google, Microsoft, Amazon, Flipkart.""",

    """Machine Learning Engineer Career in India:
    Essential Skills: Python, Machine Learning, Deep Learning,
    Mathematics, Statistics, Git.
    Important Skills: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Docker.
    Salary: Fresher 6-10 LPA, 1-2 years 10-20 LPA, 3-5 years 20-40 LPA.
    Learning Path: Python → Statistics → ML → Deep Learning → Projects.""",

    """Interview Preparation Guide for Indian Tech Jobs:
    DSA: Practice LeetCode daily. Focus on Arrays, Trees, Graphs, DP.
    System Design: Load balancing, Caching, Databases.
    Behavioral: Use STAR format - Situation, Task, Action, Result.
    Tips: Company research karo, GitHub update rakho, Mock interviews karo.""",

    """Resume Writing Tips for Indian Tech Freshers:
    Format: 1 page maximum, PDF format.
    Sections: Contact, Skills, Projects, Education, Certifications.
    Action Verbs: Built, Developed, Implemented, Designed, Optimized.
    Projects: Tech stack mention karo, GitHub link dalo.
    ATS: Job description keywords use karo.""",

    """LangChain and RAG Systems:
    LangChain = Framework for LLM applications.
    RAG = Retrieval Augmented Generation.
    Components: Document Loaders, Embeddings, Vector Stores, LLMs, Agents.
    Vector DBs: FAISS, ChromaDB, Pinecone, Weaviate.
    Use Cases: Document Q&A, Chatbots, Knowledge Management.""",

    """Defence AI Career Opportunities in India:
    Organizations: DRDO, IAF, Indian Navy, ISRO, BEL, HAL.
    Required Skills: Python, Computer Vision, Signal Processing,
    Embedded Systems, Machine Learning, Edge AI.
    Entry Points: DRDO internships, UDAAN program (IAF), iDEX startups.
    Salary: DRDO Scientist B 7-15 LPA, Private defence 8-20 LPA.""",

    """Salary Negotiation Tips for Indian Tech Jobs:
    Research: Glassdoor, AmbitionBox, LinkedIn salary insights.
    Strategy: Never reveal current salary, give range not exact number.
    How much: Entry level 10-15% above offer, Mid level 15-25% above.
    Total Compensation: Fixed salary, Variable, ESOPs, Health insurance.""",

    """Python for Machine Learning - Complete Guide:
    NumPy: Array operations, Mathematical functions, Linear algebra.
    Pandas: Data manipulation, CSV reading, Data cleaning, EDA.
    Scikit-learn: Classical ML algorithms, Model training, Evaluation.
    TensorFlow/Keras: Deep Learning, Neural networks, GPU training.
    PyTorch: Research-focused, Dynamic graphs, Popular in academia."""
]

METADATAS = [
    {"category": "career", "topic": "software_engineering"},
    {"category": "career", "topic": "ml_engineering"},
    {"category": "interview", "topic": "preparation"},
    {"category": "resume", "topic": "tips"},
    {"category": "technical", "topic": "langchain_rag"},
    {"category": "career", "topic": "defence_ai"},
    {"category": "career", "topic": "salary"},
    {"category": "technical", "topic": "python_ml"}
]

if __name__ == "__main__":
    print("=" * 50)
    print("Career Knowledge Base Ingestion")
    print("=" * 50)
    print(f"Total documents: {len(CAREER_DOCUMENTS)}")
    print()

    success = create_vector_store(
        documents=CAREER_DOCUMENTS,
        metadatas=METADATAS
    )

    if success:
        print()
        print("✅ Knowledge base ready hai!")
    else:
        print("❌ Ingestion failed!")