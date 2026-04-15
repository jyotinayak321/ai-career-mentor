# ================================================
# roadmap.py — Career Roadmap Generator API
# ================================================
# ENDPOINT:
# POST /api/roadmap/generate
# GET  /api/roadmap/my-roadmap
# ================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.auth import get_current_user
from skill_gap.detector import detect_skill_gap
from database.mongodb import get_db
from typing import Optional, List
import datetime

router = APIRouter()


# Request model
class RoadmapRequest(BaseModel):
    target_role: str
    timeline_weeks: Optional[int] = 12
    focus_areas: Optional[List[str]] = []


# ------------------------------------------------
# ROUTE 1 — Generate Roadmap
# ------------------------------------------------

@router.post("/generate")
async def generate_roadmap(
    request: RoadmapRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Personalized career roadmap generate karo

    User ki skills + Target role + Timeline
    = Weekly learning plan
    """

    user_skills = current_user.get("skills", [])

    # Skill gap detect karo
    gap = detect_skill_gap(
        user_skills,
        request.target_role
    )

    missing_essential = gap["gap_analysis"]["missing_essential"]
    missing_important = gap["gap_analysis"]["missing_important"]
    all_missing = missing_essential + missing_important

    # Weekly roadmap generate karo
    weekly_plan = []
    weeks = request.timeline_weeks

    # Skills ko weeks mein divide karo
    skills_per_week = max(1, len(all_missing) // weeks)

    for week in range(1, weeks + 1):

        # Is week ki skills
        start_idx = (week - 1) * skills_per_week
        end_idx = start_idx + skills_per_week
        week_skills = all_missing[start_idx:end_idx]

        if not week_skills:
            # Skills khatam ho gayi
            # Practice aur projects
            week_skills = ["Portfolio building", "Projects"]

        # Week ka theme
        if week <= weeks // 3:
            theme = "Foundation Building"
            phase = "Phase 1 — Core Skills"
        elif week <= (weeks * 2) // 3:
            theme = "Skill Development"
            phase = "Phase 2 — Advanced Skills"
        else:
            theme = "Project Building"
            phase = "Phase 3 — Application"

        weekly_plan.append({
            "week": week,
            "phase": phase,
            "theme": theme,
            "skills_to_learn": week_skills,
            "resources": _get_week_resources(week_skills),
            "project": _get_week_project(week, week_skills),
            "goal": f"Complete {', '.join(week_skills[:2])} basics"
        })

    # Milestone projects
    milestones = [
        {
            "month": 1,
            "project": f"Basic {request.target_role} Project",
            "description": "Core skills use karke ek simple project",
            "tech_stack": missing_essential[:3]
        },
        {
            "month": 2,
            "project": "Intermediate Project",
            "description": "Advanced features add karo",
            "tech_stack": missing_important[:3]
        },
        {
            "month": 3,
            "project": "Portfolio Project",
            "description": "Production-grade project for portfolio",
            "tech_stack": user_skills[:3] + missing_essential[:2]
        }
    ]

    # Database mein save karo
    db = get_db()
    roadmap_doc = {
        "user_id": str(current_user["_id"]),
        "target_role": request.target_role,
        "timeline_weeks": weeks,
        "weekly_plan": weekly_plan,
        "milestones": milestones,
        "created_at": datetime.datetime.utcnow()
    }
    await db.roadmaps.insert_one(roadmap_doc)

    return {
        "message": "Roadmap ready hai! 🗺️",
        "target_role": request.target_role,
        "timeline": f"{weeks} weeks",
        "current_match": f"{gap['match_percentage']}%",
        "missing_skills": all_missing,
        "weekly_plan": weekly_plan,
        "milestones": milestones,
        "summary": gap["summary"]
    }


# ------------------------------------------------
# ROUTE 2 — My Roadmap
# ------------------------------------------------

@router.get("/my-roadmap")
async def get_my_roadmap(
    current_user: dict = Depends(get_current_user)
):
    """User ka latest roadmap lo"""
    db = get_db()

    roadmap = await db.roadmaps.find_one(
        {"user_id": str(current_user["_id"])},
        sort=[("created_at", -1)]
    )

    if not roadmap:
        return {
            "message": "Koi roadmap nahi mila. Pehle generate karo!",
            "roadmap": None
        }

    roadmap["_id"] = str(roadmap["_id"])

    return {
        "message": "Tumhara roadmap!",
        "roadmap": roadmap
    }


# ------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------

def _get_week_resources(skills: List[str]) -> List[str]:
    """Skills ke liye resources suggest karo"""
    resource_map = {
        "python": "freeCodeCamp Python Course",
        "machine learning": "Coursera ML — Andrew Ng",
        "deep learning": "Fast.ai Course",
        "docker": "Docker Official Documentation",
        "aws": "AWS Free Tier + Documentation",
        "react": "React Official Docs (react.dev)",
        "sql": "SQLZoo + LeetCode SQL",
        "data structures": "LeetCode + GeeksforGeeks",
        "system design": "Grokking System Design",
        "langchain": "LangChain Documentation",
        "tensorflow": "TensorFlow Official Tutorials",
        "pytorch": "PyTorch Official Tutorials"
    }

    resources = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in resource_map:
            resources.append(resource_map[skill_lower])
        else:
            resources.append(
                f"YouTube: {skill} tutorial"
            )

    return resources[:3]


def _get_week_project(
    week: int,
    skills: List[str]
) -> str:
    """Week ke liye project suggest karo"""
    projects = [
        "CLI tool banao skills use karke",
        "REST API banao",
        "Simple web app banao",
        "Data analysis project",
        "ML model train karo",
        "Portfolio website update karo",
        "GitHub pe push karo",
        "Documentation likho"
    ]

    idx = (week - 1) % len(projects)
    skill = skills[0] if skills else "learned skills"

    return f"{projects[idx]} — {skill} use karke"