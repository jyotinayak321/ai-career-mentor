# ================================================
# interview.py — Mock Interview API
# ================================================
# ENDPOINTS:
# POST /api/interview/start   — Interview shuru
# POST /api/interview/answer  — Answer submit
# GET  /api/interview/history — History dekho
# ================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.auth import get_current_user
from database.mongodb import get_db
from agents.career_agent import client
from config import settings
from typing import Optional, List
import datetime
import json

router = APIRouter()


# Request models
class StartInterview(BaseModel):
    role: str
    difficulty: Optional[str] = "medium"
    num_questions: Optional[int] = 5

class SubmitAnswer(BaseModel):
    session_id: str
    question_id: int
    question: str
    answer: str


# ------------------------------------------------
# ROUTE 1 — Start Interview
# ------------------------------------------------

@router.post("/start")
async def start_interview(
    request: StartInterview,
    current_user: dict = Depends(get_current_user)
):
    """
    Mock interview session shuru karo
    Groq se questions generate karo
    """

    user_skills = current_user.get("skills", [])
    skills_str = ", ".join(user_skills[:8]) if user_skills else request.role

    # Groq se questions generate karo
    prompt = f"""Generate {request.num_questions} interview questions 
for a {request.role} position.

Candidate skills: {skills_str}
Difficulty: {request.difficulty}

Return ONLY a JSON array:
[
  {{
    "id": 1,
    "category": "Technical/Behavioral/HR",
    "question": "question text here",
    "hints": ["hint 1", "hint 2"],
    "difficulty": "{request.difficulty}"
  }}
]

Mix technical, behavioral, and HR questions.
Make them relevant to Indian job market."""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        response_text = response.choices[0].message.content

        # JSON extract karo
        import re
        json_match = re.search(
            r'\[.*\]',
            response_text,
            re.DOTALL
        )

        if json_match:
            questions = json.loads(json_match.group())
        else:
            questions = _get_default_questions(
                request.role,
                request.num_questions
            )

    except Exception as e:
        print(f"Question generation error: {e}")
        questions = _get_default_questions(
            request.role,
            request.num_questions
        )

    # Session database mein save karo
    db = get_db()
    session = {
        "user_id": str(current_user["_id"]),
        "role": request.role,
        "difficulty": request.difficulty,
        "questions": questions,
        "answers": [],
        "status": "in_progress",
        "started_at": datetime.datetime.utcnow()
    }

    result = await db.interview_sessions.insert_one(session)
    session_id = str(result.inserted_id)

    return {
        "message": "Interview shuru! All the best! 🎯",
        "session_id": session_id,
        "role": request.role,
        "total_questions": len(questions),
        "questions": questions,
        "instructions": [
            "Har question ka detailed answer do",
            "Examples aur projects mention karo",
            "STAR format use karo behavioral questions mein"
        ]
    }


# ------------------------------------------------
# ROUTE 2 — Submit Answer
# ------------------------------------------------

@router.post("/answer")
async def submit_answer(
    request: SubmitAnswer,
    current_user: dict = Depends(get_current_user)
):
    """
    Answer submit karo aur AI feedback lo
    """

    # Groq se answer evaluate karo
    eval_prompt = f"""You are a senior technical interviewer.

Question: {request.question}

Candidate's Answer: {request.answer}

Evaluate this answer and respond in JSON:
{{
  "score": 7,
  "out_of": 10,
  "strengths": ["What was good about the answer"],
  "improvements": ["What could be better"],
  "ideal_answer_hint": "Key points that should be covered",
  "follow_up": "A follow-up question"
}}

Be constructive and encouraging."""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "user", "content": eval_prompt}
            ],
            max_tokens=800,
            temperature=0.5
        )

        response_text = response.choices[0].message.content

        import re
        json_match = re.search(
            r'\{.*\}',
            response_text,
            re.DOTALL
        )

        if json_match:
            feedback = json.loads(json_match.group())
        else:
            feedback = {
                "score": 7,
                "out_of": 10,
                "strengths": ["Good attempt!"],
                "improvements": ["Add more specific examples"],
                "ideal_answer_hint": "Focus on practical experience",
                "follow_up": "Can you elaborate more?"
            }

    except Exception as e:
        print(f"Evaluation error: {e}")
        feedback = {
            "score": 6,
            "out_of": 10,
            "strengths": ["Answer diya — good start!"],
            "improvements": ["Aur detail add karo"],
            "ideal_answer_hint": "Be more specific",
            "follow_up": "Tell me more about your experience"
        }

    # Database mein save karo
    db = get_db()
    from bson import ObjectId
    await db.interview_sessions.update_one(
        {"_id": ObjectId(request.session_id)},
        {"$push": {
            "answers": {
                "question_id": request.question_id,
                "question": request.question,
                "answer": request.answer,
                "feedback": feedback,
                "answered_at": datetime.datetime.utcnow()
            }
        }}
    )

    return {
        "message": "Answer evaluated!",
        "question_id": request.question_id,
        "feedback": feedback,
        "score": f"{feedback['score']}/{feedback['out_of']}"
    }


# ------------------------------------------------
# ROUTE 3 — Interview History
# ------------------------------------------------

@router.get("/history")
async def get_interview_history(
    current_user: dict = Depends(get_current_user)
):
    """User ki interview history lo"""
    db = get_db()

    sessions = await db.interview_sessions.find(
        {"user_id": str(current_user["_id"])}
    ).sort("started_at", -1).to_list(10)

    for s in sessions:
        s["_id"] = str(s["_id"])

    return {
        "total_sessions": len(sessions),
        "sessions": sessions
    }


# ------------------------------------------------
# DEFAULT QUESTIONS
# ------------------------------------------------

def _get_default_questions(
    role: str,
    n: int
) -> List[dict]:
    """Fallback questions"""
    questions = [
        {
            "id": 1,
            "category": "HR",
            "question": "Tell me about yourself and your journey into tech.",
            "hints": ["Background", "Skills", "Projects", "Goals"],
            "difficulty": "easy"
        },
        {
            "id": 2,
            "category": "Technical",
            "question": f"Explain your most challenging project as a {role}.",
            "hints": ["Problem", "Solution", "Tech stack", "Result"],
            "difficulty": "medium"
        },
        {
            "id": 3,
            "category": "Technical",
            "question": "What is the difference between SQL and NoSQL databases?",
            "hints": ["Schema", "Scalability", "Use cases", "Examples"],
            "difficulty": "medium"
        },
        {
            "id": 4,
            "category": "Behavioral",
            "question": "Describe a situation where you had to learn something quickly.",
            "hints": ["Situation", "What you learned", "How", "Result"],
            "difficulty": "easy"
        },
        {
            "id": 5,
            "category": "HR",
            "question": "Where do you see yourself in 5 years?",
            "hints": ["Career goals", "Skills", "Company alignment"],
            "difficulty": "easy"
        }
    ]

    return questions[:n]