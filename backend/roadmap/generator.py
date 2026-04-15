# ================================================
# generator.py — Career Roadmap Generator
# ================================================
# YE FILE KYA KARTI HAI?
# User ki skills aur target role ke basis pe
# Personalized weekly learning roadmap banati hai
#
# Groq LLM use karta hai
# Intelligent, personalized plan generate karta hai
# ================================================

from agents.career_agent import client
from config import settings
from skill_gap.detector import detect_skill_gap
from typing import List, Dict
import json
import re


# ------------------------------------------------
# FUNCTION 1 — generate_with_llm()
# ------------------------------------------------
# Groq se roadmap generate karo
# ------------------------------------------------

def generate_with_llm(
    user_name: str,
    current_skills: List[str],
    target_role: str,
    missing_skills: List[str],
    timeline_weeks: int
) -> Dict:
    """
    Groq LLM se personalized roadmap generate karo

    Args:
        user_name: User ka naam
        current_skills: Jo skills hain abhi
        target_role: Jis role ke liye roadmap chahiye
        missing_skills: Jo skills seekhni hain
        timeline_weeks: Kitne weeks mein complete karna

    Returns:
        Complete roadmap dictionary
    """

    # Prompt prepare karo
    prompt = f"""You are an expert career coach for Indian tech students.

Create a detailed {timeline_weeks}-week learning roadmap for:
- Name: {user_name}
- Current Skills: {', '.join(current_skills[:8])}
- Target Role: {target_role}
- Skills to Learn: {', '.join(missing_skills[:8])}

Return ONLY a valid JSON object (no extra text):
{{
  "roadmap_title": "Journey to {target_role}",
  "total_weeks": {timeline_weeks},
  "weekly_plan": [
    {{
      "week": 1,
      "theme": "Foundation",
      "skills_to_learn": ["skill1"],
      "resources": ["Resource name (Free/Paid)"],
      "daily_tasks": ["Task 1", "Task 2"],
      "project": "Mini project to build",
      "goal": "What you will achieve"
    }}
  ],
  "milestone_projects": [
    {{
      "month": 1,
      "project_name": "Project Name",
      "tech_stack": ["tech1", "tech2"],
      "description": "What to build",
      "github_worthy": true
    }}
  ],
  "final_goal": "Where you will be after {timeline_weeks} weeks",
  "tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Rules:
- Focus on free resources first
- Include Indian platforms (NPTEL, CDAC)
- Be realistic with timeline
- Include hands-on projects every week
- Maximum {timeline_weeks} weeks in weekly_plan"""

    try:
        # Groq API call
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=3000,
            temperature=0.7
        )

        response_text = response.choices[0].message.content

        # JSON extract karo response se
        json_match = re.search(
            r'\{.*\}',
            response_text,
            re.DOTALL
        )

        if json_match:
            roadmap = json.loads(json_match.group())
            return {
                "success": True,
                "roadmap": roadmap,
                "generated_by": "Groq LLM"
            }
        else:
            print("JSON parse nahi hua, fallback use kar rahe hain")
            return {
                "success": False,
                "roadmap": _create_fallback_roadmap(
                    target_role,
                    missing_skills,
                    timeline_weeks
                ),
                "generated_by": "Fallback System"
            }

    except Exception as e:
        print(f"LLM error: {e}")
        return {
            "success": False,
            "roadmap": _create_fallback_roadmap(
                target_role,
                missing_skills,
                timeline_weeks
            ),
            "generated_by": "Fallback System"
        }


# ------------------------------------------------
# FUNCTION 2 — generate_roadmap()
# ------------------------------------------------
# Main function jo saari cheezein combine karta hai
# ------------------------------------------------

def generate_roadmap(
    user_name: str,
    user_skills: List[str],
    target_role: str,
    timeline_weeks: int = 12
) -> Dict:
    """
    Complete personalized roadmap generate karo

    Steps:
    1. Skill gap detect karo
    2. Missing skills identify karo
    3. LLM se roadmap generate karo
    4. Complete result return karo
    """

    # Step 1: Skill gap detect karo
    gap_result = detect_skill_gap(
        user_skills,
        target_role
    )

    missing_essential = gap_result["gap_analysis"]["missing_essential"]
    missing_important = gap_result["gap_analysis"]["missing_important"]
    all_missing = missing_essential + missing_important

    # Step 2: LLM se roadmap generate karo
    llm_result = generate_with_llm(
        user_name=user_name,
        current_skills=user_skills,
        target_role=target_role,
        missing_skills=all_missing[:8],
        timeline_weeks=timeline_weeks
    )

    # Step 3: Complete result return karo
    return {
        "user": user_name,
        "target_role": target_role,
        "timeline_weeks": timeline_weeks,
        "current_match": f"{gap_result['match_percentage']}%",
        "readiness": gap_result["readiness_level"],
        "missing_skills": all_missing,
        "roadmap": llm_result["roadmap"],
        "generated_by": llm_result["generated_by"],
        "skill_gap_summary": gap_result["summary"]
    }


# ------------------------------------------------
# FUNCTION 3 — _create_fallback_roadmap()
# ------------------------------------------------
# LLM fail ho toh basic roadmap return karo
# ------------------------------------------------

def _create_fallback_roadmap(
    target_role: str,
    missing_skills: List[str],
    timeline_weeks: int
) -> Dict:
    """
    Fallback roadmap — LLM ke bina
    Simple rule-based roadmap
    """

    # Resources database
    resources = {
        "python": "freeCodeCamp Python (Free)",
        "machine learning": "Coursera ML — Andrew Ng",
        "deep learning": "Fast.ai (Free)",
        "docker": "Docker Official Docs (Free)",
        "aws": "AWS Free Tier + Docs",
        "react": "React Official Docs (Free)",
        "sql": "SQLZoo (Free)",
        "data structures": "LeetCode (Free)",
        "system design": "Grokking System Design",
        "tensorflow": "TensorFlow Tutorials (Free)",
        "pytorch": "PyTorch Tutorials (Free)",
        "langchain": "LangChain Docs (Free)",
        "mathematics": "Khan Academy (Free)",
        "statistics": "StatQuest YouTube (Free)"
    }

    # Weekly plan banao
    weekly_plan = []
    skills_per_week = max(1, len(missing_skills) // timeline_weeks)

    for week in range(1, min(timeline_weeks + 1, 13)):
        start_idx = (week - 1) * skills_per_week
        week_skills = missing_skills[start_idx:start_idx + skills_per_week]

        if not week_skills:
            week_skills = ["Portfolio Building", "Interview Prep"]

        # Resources dhundo
        week_resources = []
        for skill in week_skills:
            resource = resources.get(
                skill.lower(),
                f"YouTube: {skill} tutorial (Free)"
            )
            week_resources.append(resource)

        # Phase determine karo
        if week <= timeline_weeks // 3:
            phase = "Phase 1 — Foundation"
            theme = "Core Concepts"
        elif week <= (timeline_weeks * 2) // 3:
            phase = "Phase 2 — Development"
            theme = "Skill Building"
        else:
            phase = "Phase 3 — Application"
            theme = "Projects & Portfolio"

        weekly_plan.append({
            "week": week,
            "theme": theme,
            "phase": phase,
            "skills_to_learn": week_skills,
            "resources": week_resources,
            "daily_tasks": [
                f"1 hour {week_skills[0]} study",
                "30 min practice/coding",
                "Document learnings"
            ],
            "project": f"Mini project using {week_skills[0]}",
            "goal": f"Complete {week_skills[0]} basics"
        })

    # Milestone projects
    milestones = []
    for month in range(1, (timeline_weeks // 4) + 1):
        month_skills = missing_skills[
            (month-1)*3: month*3
        ] if missing_skills else [target_role]

        milestones.append({
            "month": month,
            "project_name": f"Month {month} Project",
            "tech_stack": month_skills[:3],
            "description": (
                f"Apply month {month} learnings "
                f"in a practical project"
            ),
            "github_worthy": month >= 2
        })

    return {
        "roadmap_title": f"Journey to {target_role}",
        "total_weeks": timeline_weeks,
        "weekly_plan": weekly_plan,
        "milestone_projects": milestones,
        "final_goal": (
            f"Get hired as {target_role} "
            f"in {timeline_weeks} weeks!"
        ),
        "tips": [
            "Consistency > Intensity — Daily 2 hours better than weekend 10 hours",
            "Build projects — Theory ke saath practical karo",
            "GitHub update karo regularly",
            "LinkedIn aur portfolio maintain karo",
            "Mock interviews practice karo last month mein"
        ]
    }