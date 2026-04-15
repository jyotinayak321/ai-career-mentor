# ================================================
# agent.py — AI Agent Chat API
# ================================================
# ENDPOINT:
# POST /api/agent/chat — AI se baat karo
# ================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.auth import get_current_user
from agents.career_agent import run_agent
from typing import Optional, List

router = APIRouter()


# Request model
class ChatRequest(BaseModel):
    message: str
    use_my_skills: Optional[bool] = True


# ------------------------------------------------
# ROUTE 1 — Chat with AI Agent
# ------------------------------------------------

@router.post("/chat")
async def chat_with_agent(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    AI Career Agent se baat karo

    Agent automatically decide karta hai:
    - Skill gap analysis karna hai?
    - Jobs recommend karne hain?
    - Interview tips dene hain?
    - Salary info deni hai?
    """

    # User ki skills lo
    user_skills = []
    if request.use_my_skills:
        user_skills = current_user.get("skills", [])

    # Agent run karo
    try:
        response = run_agent(
            user_message=request.message,
            user_skills=user_skills
        )

        return {
            "message": request.message,
            "response": response,
            "user_skills_used": len(user_skills) > 0,
            "skills_count": len(user_skills)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )


# ------------------------------------------------
# ROUTE 2 — Quick Career Tips
# ------------------------------------------------

@router.get("/tips")
async def get_career_tips(
    current_user: dict = Depends(get_current_user)
):
    """
    Quick personalized career tips lo
    """
    user_skills = current_user.get("skills", [])
    resume_score = current_user.get("resume_score", 0)

    tips = []

    # Score based tips
    if resume_score < 70:
        tips.append(
            "📄 Resume improve karo — "
            "score 70+ hona chahiye"
        )

    # Skills based tips
    if len(user_skills) < 10:
        tips.append(
            "⚡ Aur skills add karo resume mein — "
            "10+ honi chahiye"
        )

    if "git" not in user_skills:
        tips.append("🔧 Git seekho — har job mein chahiye!")

    if "docker" not in user_skills:
        tips.append("🐳 Docker seekho — DevOps ke liye zaroori")

    if not any(
        cloud in user_skills
        for cloud in ["aws", "azure", "gcp"]
    ):
        tips.append("☁️ Cloud platform seekho (AWS/Azure)")

    # General tips
    tips.extend([
        "💻 LeetCode pe daily practice karo",
        "🚀 GitHub projects update rakho",
        "🔗 LinkedIn profile complete karo",
        "📚 Tech blogs padhte raho"
    ])

    return {
        "user": current_user.get("name"),
        "resume_score": resume_score,
        "skills_count": len(user_skills),
        "personalized_tips": tips[:6]
    }