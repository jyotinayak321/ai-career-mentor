# ================================================
# recommender.py — Job Recommendation Engine
# ================================================
# YE FILE KYA KARTI HAI?
# User ki skills ke basis pe jobs recommend karta hai
#
# FLOW:
# 1. mock_jobs.json se saari jobs load karo
# 2. Har job ka match score calculate karo
# 3. Role filter se bonus score do
# 4. Sort karke top jobs return karo
# ================================================

import json
import os
from typing import List, Dict


# ------------------------------------------------
# FUNCTION 1 — load_jobs()
# ------------------------------------------------
# mock_jobs.json se jobs load karo
# Ye JSON file mein 20+ jobs hain
# Har job mein: title, company, skills, links
# ------------------------------------------------

def load_jobs() -> List[Dict]:
    """
    JSON file se saari jobs load karo

    os.path.dirname(__file__) = Is file ki directory
    Matlab: job_recommender/ folder
    """

    # Is file ki directory dhundo
    current_dir = os.path.dirname(__file__)

    # JSON file ka full path banao
    jobs_file = os.path.join(
        current_dir,
        "mock_jobs.json"
    )

    # File open karo aur parse karo
    with open(jobs_file, "r") as f:
        jobs = json.load(f)

    print(f"✅ {len(jobs)} jobs loaded!")
    return jobs


# ------------------------------------------------
# FUNCTION 2 — calculate_match_score()
# ------------------------------------------------
# User skills aur job required skills ka
# match percentage calculate karo
#
# FORMULA:
# matched_skills / total_required_skills * 100
#
# EXAMPLE:
# Job needs:  [python, docker, aws, sql] = 4
# User has:   [python, react, docker]
# Matched:    [python, docker] = 2
# Score:      2/4 * 100 = 50%
# ------------------------------------------------

def calculate_match_score(
    user_skills: List[str],
    job_skills: List[str]
) -> float:
    """
    Skills match percentage calculate karo

    Args:
        user_skills: User ki skills list
        job_skills: Job ki required skills

    Returns:
        Match percentage (0-100)
    """

    # Agar job mein koi skills nahi
    # toh 50% default score do
    if not job_skills:
        return 50.0

    # Lowercase sets banao
    # Set = Fast lookup (O(1) time)
    # No duplicates allowed
    user_set = set(s.lower() for s in user_skills)
    job_set = set(s.lower() for s in job_skills)

    # Common skills dhundo
    # & = Set intersection operator
    # user_set & job_set = Dono mein common skills
    matched = user_set & job_set

    # Percentage calculate karo
    score = (len(matched) / len(job_set)) * 100

    # Round to 1 decimal place
    return round(score, 1)


# ------------------------------------------------
# FUNCTION 3 — recommend_jobs()
# ------------------------------------------------
# Main function jo saari jobs process karta hai
# Aur user ke liye best matches return karta hai
#
# min_match = 0.0 kyunki:
# Pehle saari jobs dikhao
# User filter kar sakta hai baad mein
# ------------------------------------------------

def recommend_jobs(
    user_skills: List[str],
    target_role: str = "",
    location: str = "",
    remote_only: bool = False,
    job_type: str = "",
    min_match: float = 0.0,  # 0% = Saari jobs dikhao
    top_n: int = 20           # Top 20 jobs return karo
) -> Dict:
    """
    User ke liye best matching jobs recommend karo

    Args:
        user_skills: User ki current skills
        target_role: Preferred job title (optional)
        location: Preferred city (optional)
        remote_only: Sirf remote jobs chahiye?
        job_type: Full Time / Internship filter
        min_match: Minimum match % (0 = sab dikhao)
        top_n: Kitni jobs return karni hain

    Returns:
        Dictionary with jobs list and metadata
    """

    # ----------------------------------------
    # STEP 1 — Saari jobs load karo
    # ----------------------------------------
    all_jobs = load_jobs()

    # Results store karne ke liye empty list
    scored_jobs = []

    # ----------------------------------------
    # STEP 2 — Har job process karo
    # ----------------------------------------
    for job in all_jobs:

        # Job ki required skills lo
        required_skills = job.get(
            'required_skills', []
        )

        # ----------------------------------------
        # Match score calculate karo
        # ----------------------------------------
        match_score = calculate_match_score(
            user_skills,
            required_skills
        )

        # ----------------------------------------
        # ROLE FILTER BONUS
        # ----------------------------------------
        # Agar user ne specific role search kiya
        # Aur job title mein woh role hai
        # Toh extra score do!
        #
        # Example:
        # User searches: "ML Engineer"
        # Job title: "Machine Learning Engineer"
        # → Partial match → +10 bonus!
        # ----------------------------------------
        if target_role:
            role_lower = target_role.lower()
            title_lower = job.get('title', '').lower()

            # Exact match mein zyada bonus
            if role_lower in title_lower:
                # +20 bonus, max 100
                match_score = min(
                    match_score + 20, 100
                )
            # Partial word match mein thoda bonus
            elif any(
                word in title_lower
                for word in role_lower.split()
            ):
                # +10 bonus, max 100
                match_score = min(
                    match_score + 10, 100
                )

        # ----------------------------------------
        # MATCHED aur MISSING SKILLS FIND KARO
        # ----------------------------------------
        user_set = set(
            s.lower() for s in user_skills
        )
        job_set = set(
            s.lower() for s in required_skills
        )

        # User ke paas jo skills hain
        matched = list(user_set & job_set)

        # User ke paas jo skills nahi hain
        missing = list(job_set - user_set)

        # ----------------------------------------
        # JOB OBJECT BANAO — Saari info ek jagah
        # ----------------------------------------
        # **job = Job ki saari existing fields
        # Plus additional computed fields
        scored_jobs.append({
            # Job ki original saari fields
            **job,

            # Computed fields
            "match_score": match_score,

            # Top 5 matched skills dikhao
            "matched_skills": matched[:5],

            # Top 3 missing skills dikhao
            # (Zyada dikhane se overwhelming lagta)
            "missing_skills": missing[:3],
        })

    # ----------------------------------------
    # STEP 3 — Score ke basis pe sort karo
    # ----------------------------------------
    # key = Sorting ka criteria
    # lambda = Anonymous function
    # reverse=True = Highest score pehle
    scored_jobs.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    # ----------------------------------------
    # STEP 4 — Top N results lo
    # ----------------------------------------
    # Slice karo first top_n elements
    top_jobs = scored_jobs[:top_n]

    # ----------------------------------------
    # STEP 5 — Result dictionary return karo
    # ----------------------------------------
    return {
        # Total kitni jobs mili
        "total_jobs_found": len(scored_jobs),

        # Kitni jobs return kar rahe hain
        "showing": len(top_jobs),

        # Jobs list
        "jobs": top_jobs,

        # Highest match score
        "top_match": (
            top_jobs[0]["match_score"]
            if top_jobs else 0
        )
    }