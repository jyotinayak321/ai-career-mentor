# ================================================
# career_agent.py — AI Career Agent (Groq Free!)
# ================================================
# YE FILE KYA KARTI HAI?
# Groq AI (Free LLaMA model) use karta hai
# User ki query ka intelligent answer deta hai
# Tools use karke accurate data leta hai
# ================================================

import json
import os
from typing import List, Dict
from groq import Groq
from config import settings
from skill_gap.detector import detect_skill_gap
from job_recommender.recommender import recommend_jobs


# ------------------------------------------------
# GROQ CLIENT BANAO
# ------------------------------------------------
# Groq = Free AI API
# LLaMA 3.3 70B model use karta hai
# Anthropic jaisi quality — bilkul free!
# ------------------------------------------------

client = Groq(
    api_key=settings.GROQ_API_KEY
)


# ------------------------------------------------
# CAREER KNOWLEDGE BASE
# ------------------------------------------------

CAREER_KNOWLEDGE = {
    "salary": {
        "software engineer": "Fresher: 4-8 LPA, 1-2 years: 8-15 LPA, 3-5 years: 15-30 LPA",
        "ml engineer": "Fresher: 6-10 LPA, 1-2 years: 10-20 LPA, 3-5 years: 20-40 LPA",
        "data scientist": "Fresher: 5-9 LPA, 1-2 years: 9-16 LPA, 3-5 years: 16-30 LPA",
        "frontend developer": "Fresher: 3-7 LPA, 1-2 years: 7-14 LPA, 3-5 years: 14-25 LPA",
        "backend developer": "Fresher: 4-8 LPA, 1-2 years: 8-16 LPA, 3-5 years: 16-30 LPA",
    },
    "skills_2024": (
        "Most demanded skills 2024: Python, JavaScript, "
        "React, AWS, Docker, Machine Learning, "
        "LangChain, GenAI, FastAPI, MongoDB"
    ),
    "defence_ai": (
        "DRDO, IAF mein AI roles growing hain. "
        "Key skills: Python, Computer Vision, "
        "Signal Processing, Embedded Systems. "
        "CDAC certification helpful hai. "
        "UDAAN program aur DRDO internships "
        "great entry points hain."
    ),
    "interview_tips": (
        "DSA practice karo daily LeetCode pe. "
        "System Design seekho senior roles ke liye. "
        "STAR format use karo behavioral questions mein. "
        "Company research zaroor karo. "
        "Mock interviews practice karo. "
        "GitHub aur LinkedIn update rakho."
    ),
    "career_path": {
        "ai_ml": "Python → Statistics → ML Basics → Deep Learning → Projects → Portfolio → Apply",
        "web": "HTML/CSS → JavaScript → React → Node.js → Projects → Apply",
        "data": "Excel → SQL → Python → Statistics → Visualization → ML → Apply",
        "backend": "Python → FastAPI → SQL → MongoDB → Docker → AWS → Apply"
    }
}


# ------------------------------------------------
# TOOL FUNCTIONS
# ------------------------------------------------

def search_career_info(
    query: str,
    category: str = "general"
) -> str:
    """Career knowledge se info lo"""

    query_lower = query.lower()
    response_parts = []

    # Salary query
    if any(w in query_lower for w in
           ["salary", "pay", "ctc", "lpa", "package"]):
        for role, sal in CAREER_KNOWLEDGE["salary"].items():
            if any(r in query_lower for r in role.split()):
                response_parts.append(
                    f"{role.title()}: {sal}"
                )
        if not response_parts:
            for role, sal in CAREER_KNOWLEDGE["salary"].items():
                response_parts.append(f"{role.title()}: {sal}")

    # Defence AI
    elif any(w in query_lower for w in
             ["defence", "defense", "iaf", "drdo"]):
        response_parts.append(CAREER_KNOWLEDGE["defence_ai"])

    # Interview
    elif any(w in query_lower for w in
             ["interview", "prepare", "question"]):
        response_parts.append(CAREER_KNOWLEDGE["interview_tips"])

    # Career path
    elif any(w in query_lower for w in
             ["career", "path", "roadmap", "start"]):
        for path, info in CAREER_KNOWLEDGE["career_path"].items():
            response_parts.append(f"{path}: {info}")

    # Skills
    elif any(w in query_lower for w in
             ["skill", "technology", "learn", "2024"]):
        response_parts.append(CAREER_KNOWLEDGE["skills_2024"])

    else:
        response_parts.append(
            CAREER_KNOWLEDGE["skills_2024"]
        )

    return "\n".join(response_parts)


def run_skill_gap_analysis(
    user_skills: List[str],
    target_role: str
) -> str:
    """Skill gap analysis run karo"""
    result = detect_skill_gap(user_skills, target_role)

    return (
        f"Skill Gap for {result['target_role']}:\n"
        f"Match: {result['match_percentage']}% "
        f"— {result['readiness_level']}\n"
        f"Matched: {', '.join(result['matched_skills'][:5])}\n"
        f"Missing Essential: "
        f"{', '.join(result['gap_analysis']['missing_essential'])}\n"
        f"Missing Important: "
        f"{', '.join(result['gap_analysis']['missing_important'][:3])}\n"
        f"Summary: {result['summary']}"
    )


def run_job_recommendations(
    user_skills: List[str],
    target_role: str = "",
    location: str = ""
) -> str:
    """Job recommendations run karo"""
    result = recommend_jobs(
        user_skills=user_skills,
        target_role=target_role,
        location=location,
        min_match=30.0,
        top_n=5
    )

    jobs_text = []
    for job in result['jobs'][:5]:
        jobs_text.append(
            f"• {job['title']} at {job['company']} "
            f"({job['match_score']}% match) — "
            f"{job['salary']} — {job['location']}"
        )

    return (
        f"Total Jobs: {result['total_jobs_found']}\n"
        f"Top Match: {result['top_match']}%\n\n"
        f"Jobs:\n" + "\n".join(jobs_text)
    )


def get_interview_tips(
    role: str,
    skills: List[str] = None
) -> str:
    """Interview tips do"""
    skills_str = (
        ", ".join(skills[:5]) if skills else role
    )

    return f"""Interview Tips for {role}:

Technical:
- DSA: LeetCode medium level daily
- Focus on: {skills_str}
- Projects clearly explain karo

Common Questions:
- Tell me about yourself
- Challenging problem solved karo
- Why this company?

Behavioral (STAR format):
- Situation → Task → Action → Result

Tips:
- Company research zaroor karo
- GitHub update rakho
- Mock interviews practice karo"""


def get_salary_info(
    role: str,
    experience: str = "fresher"
) -> str:
    """Salary info do"""
    role_lower = role.lower()

    for r, sal in CAREER_KNOWLEDGE["salary"].items():
        if r in role_lower or role_lower in r:
            return (
                f"Salary for {role}:\n"
                f"Experience: {experience}\n"
                f"{sal}\n\n"
                f"Tips:\n"
                f"• Hamesha negotiate karo\n"
                f"• 10-15% upar maango\n"
                f"• FAANG 20-50% more deti hain"
            )

    return "Glassdoor ya AmbitionBox check karo!"


# ------------------------------------------------
# MAIN FUNCTION — run_agent()
# ------------------------------------------------

def run_agent(
    user_message: str,
    user_skills: List[str] = None,
    chat_history: List = None
) -> str:
    """
    Groq AI Agent run karo

    Kaise kaam karta hai:
    1. User message + skills context bhejo
    2. Relevant tools run karo
    3. Context ke saath Groq ko bhejo
    4. Groq intelligent response banata hai
    """

    # System prompt
    system_prompt = """You are an expert AI Career Mentor 
for Indian tech students and job seekers.

You help with career guidance, skill gaps, 
job recommendations, interview prep, and salary info.

Guidelines:
- Be friendly and encouraging
- Always respond in ENGLISH only
- Be specific and actionable  
- Focus on Indian job market
- Always motivate the user!
- Keep responses concise but helpful"""

    # ----------------------------------------
    # CONTEXT GATHER KARO
    # ----------------------------------------
    # Tools se relevant data nikalo
    # Groq ko context ke saath bhejo

    context_parts = []

    if user_skills:
        # Skill gap info
        try:
            gap_result = detect_skill_gap(
                user_skills,
                "software engineer"
            )
            context_parts.append(
                f"User Skill Gap Info:\n"
                f"{gap_result['summary']}\n"
                f"Match: {gap_result['match_percentage']}%"
            )
        except Exception as e:
            print(f"Skill gap error: {e}")

        # Job recommendations
        try:
            jobs_result = recommend_jobs(
                user_skills=user_skills,
                min_match=40.0,
                top_n=3
            )
            if jobs_result['jobs']:
                top_jobs = [
                    f"{j['title']} at {j['company']} "
                    f"({j['match_score']}% match)"
                    for j in jobs_result['jobs'][:3]
                ]
                context_parts.append(
                    f"Top Matching Jobs:\n"
                    + "\n".join(top_jobs)
                )
        except Exception as e:
            print(f"Jobs error: {e}")

    # Message specific context
    msg_lower = user_message.lower()

    if any(w in msg_lower for w in
           ["salary", "pay", "ctc", "lpa"]):
        context_parts.append(
            search_career_info("salary information")
        )

    elif any(w in msg_lower for w in
             ["interview", "prepare", "question"]):
        role = "Software Engineer"
        if user_skills:
            context_parts.append(
                get_interview_tips(role, user_skills)
            )

    elif any(w in msg_lower for w in
             ["defence", "defense", "iaf", "drdo"]):
        context_parts.append(
            search_career_info("defence AI careers")
        )

    # ----------------------------------------
    # GROQ KO CALL KARO
    # ----------------------------------------

    # Full message with context
    full_message = user_message

    if user_skills:
        full_message += (
            f"\n\nMy Skills: {', '.join(user_skills)}"
        )

    if context_parts:
        full_message += (
            "\n\nRelevant Context:\n" +
            "\n\n".join(context_parts)
        )

    try:
        # Groq API call
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": full_message
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq Error: {e}")
        return (
            "AI response generate nahi ho saka. "
            "Please retry karein."
        )


# ------------------------------------------------
# EXECUTE TOOL — Backward compatibility
# ------------------------------------------------

def execute_tool(
    tool_name: str,
    tool_input: Dict
) -> str:
    """Tool execute karo"""

    if tool_name == "search_career_info":
        return search_career_info(
            tool_input.get("query", "")
        )
    elif tool_name == "analyze_skill_gap":
        return run_skill_gap_analysis(
            tool_input.get("user_skills", []),
            tool_input.get("target_role", "software engineer")
        )
    elif tool_name == "get_job_recommendations":
        return run_job_recommendations(
            tool_input.get("user_skills", []),
            tool_input.get("target_role", ""),
            tool_input.get("location", "")
        )
    elif tool_name == "get_interview_tips":
        return get_interview_tips(
            tool_input.get("role", ""),
            tool_input.get("skills", [])
        )
    elif tool_name == "get_salary_info":
        return get_salary_info(
            tool_input.get("role", ""),
            tool_input.get("experience", "fresher")
        )
    else:
        return f"Tool '{tool_name}' nahi mila!"