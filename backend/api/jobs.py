# ================================================
# jobs.py — Job Recommendation API
# ================================================

from fastapi import APIRouter, Depends, Query
from api.auth import get_current_user
from job_recommender.recommender import recommend_jobs
from job_recommender.real_jobs import fetch_real_jobs
from skill_gap.detector import detect_skill_gap
from typing import Optional

router = APIRouter()

# Default skills agar resume upload nahi kiya
DEFAULT_SKILLS = [
    "python", "machine learning", "javascript",
    "react", "mongodb", "git", "sql", "docker",
    "langchain", "fastapi", "deep learning"
]


@router.get("/recommend")
async def get_job_recommendations(
    role: Optional[str] = Query(default=""),
    location: Optional[str] = Query(default="India"),
    remote: Optional[bool] = Query(default=False),
    use_real: Optional[bool] = Query(default=True),
    current_user: dict = Depends(get_current_user)
):
    """
    Jobs recommend karo:
    1. Pehle real jobs try karo (JSearch API)
    2. Agar fail ho toh mock jobs use karo
    3. AI se match score calculate karo
    """

    # User ki skills lo
    user_skills = current_user.get("skills", [])

    # Agar skills nahi hain toh defaults use karo
    if not user_skills:
        user_skills = DEFAULT_SKILLS

    all_jobs = []

    # ----------------------------------------
    # STEP 1 — Real Jobs fetch karo
    # ----------------------------------------
    if use_real:
        try:
            search_query = role or "software engineer"
            real_jobs = await fetch_real_jobs(
                query=search_query,
                location=location or "India",
                num_pages=2
            )

            if real_jobs:
                print(f"✅ {len(real_jobs)} real jobs mili!")

                # Match score calculate karo
                for job in real_jobs:
                    required = job.get(
                        "required_skills", []
                    )

                    # Skills match karo
                    user_set = set(
                        s.lower() for s in user_skills
                    )
                    job_set = set(
                        s.lower() for s in required
                    )

                    matched = list(user_set & job_set)
                    missing = list(job_set - user_set)

                    # Score calculate
                    if job_set:
                        score = round(
                            len(matched) / len(job_set) * 100, 1
                        )
                    else:
                        score = 50.0

                    job["match_score"] = score
                    job["matched_skills"] = matched[:5]
                    job["missing_skills"] = missing[:3]

                all_jobs = real_jobs

        except Exception as e:
            print(f"Real jobs error: {e}")

    # ----------------------------------------
    # STEP 2 — Mock jobs bhi add karo
    # ----------------------------------------
    mock_result = recommend_jobs(
        user_skills=user_skills,
        target_role=role or "",
        location="",
        min_match=0.0,
        top_n=15
    )

    mock_jobs = mock_result.get("jobs", [])

    # Real jobs ke saath mock jobs combine karo
    # Duplicates avoid karo
    if all_jobs:
        # Real jobs pehle, mock baad mein
        all_jobs = all_jobs + mock_jobs[:5]
    else:
        # Sirf mock jobs
        all_jobs = mock_jobs

    # ----------------------------------------
    # STEP 3 — Sort by match score
    # ----------------------------------------
    all_jobs.sort(
        key=lambda x: x.get("match_score", 0),
        reverse=True
    )

    # ----------------------------------------
    # STEP 4 — Skill gap info
    # ----------------------------------------
    try:
        gap_result = detect_skill_gap(
            user_skills,
            role or "software engineer"
        )
        skill_info = {
            "match_percentage": gap_result["match_percentage"],
            "readiness": gap_result["readiness_level"]
        }
    except Exception as e:
        print(f"Skill gap error: {e}")
        skill_info = {
            "match_percentage": 50,
            "readiness": "Intermediate"
        }

    return {
        "message": f"{len(all_jobs)} jobs mili!",
        "user_skills": user_skills,
        "skill_match_info": skill_info,
        "total_jobs": len(all_jobs),
        "real_jobs_count": len(
            [j for j in all_jobs if j.get("source") == "real"]
        ),
        "jobs": all_jobs[:25]
    }


@router.get("/analysis")
async def get_career_analysis(
    target_role: Optional[str] = Query(
        default="software engineer"
    ),
    current_user: dict = Depends(get_current_user)
):
    """Complete career analysis"""

    user_skills = current_user.get("skills", [])
    if not user_skills:
        user_skills = DEFAULT_SKILLS

    gap = detect_skill_gap(user_skills, target_role)
    jobs = recommend_jobs(
        user_skills=user_skills,
        min_match=0.0,
        top_n=5
    )

    return {
        "target_role": target_role,
        "skill_gap": gap,
        "job_recommendations": jobs,
        "summary": {
            "match_percentage": gap["match_percentage"],
            "readiness": gap["readiness_level"],
            "top_job": (
                jobs["jobs"][0]["title"]
                if jobs["jobs"] else "No match"
            ),
            "top_match": jobs["top_match"]
        }
    }