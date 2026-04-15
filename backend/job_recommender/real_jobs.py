# ================================================
# real_jobs.py — Real Jobs from JSearch API
# ================================================
# RapidAPI JSearch se real jobs fetch karta hai
# LinkedIn, Indeed, Glassdoor se data aata hai
# ================================================

import httpx
from config import settings
from typing import List, Dict


# ------------------------------------------------
# FUNCTION 1 — fetch_real_jobs()
# ------------------------------------------------
# JSearch API se real jobs fetch karo
# ------------------------------------------------

async def fetch_real_jobs(
    query: str = "software engineer",
    location: str = "India",
    num_pages: int = 2
) -> List[Dict]:
    """
    JSearch API se real jobs fetch karo

    Args:
        query: Job search query
        location: Job location
        num_pages: Kitne pages fetch karne hain

    Returns:
        List of real jobs
    """

    # API key check karo
    if not settings.RAPIDAPI_KEY:
        print("RapidAPI key nahi hai! Mock jobs use karenge.")
        return []

    try:
        # JSearch API headers
        headers = {
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
            "X-RapidAPI-Host": settings.RAPIDAPI_HOST
        }

        # Search query banao
        search_query = f"{query} in {location}"

        # API call karo
        url = "https://jsearch.p.rapidapi.com/search"
        params = {
            "query": search_query,
            "page": "1",
            "num_pages": str(num_pages),
            "country": "in",
            "date_posted": "month"
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                url,
                headers=headers,
                params=params
            )

        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            return []

        data = response.json()
        raw_jobs = data.get("data", [])

        print(f"✅ {len(raw_jobs)} real jobs fetched!")

        # Jobs format karo
        formatted_jobs = []
        for job in raw_jobs:
            formatted = format_job(job)
            if formatted:
                formatted_jobs.append(formatted)

        return formatted_jobs

    except Exception as e:
        print(f"Real jobs fetch error: {e}")
        return []


# ------------------------------------------------
# FUNCTION 2 — format_job()
# ------------------------------------------------
# JSearch response ko hamare format mein convert
# ------------------------------------------------

def format_job(job: Dict) -> Dict:
    """
    JSearch job data ko hamare format mein convert karo
    """
    try:
        # Apply links banao
        apply_link = job.get(
            "job_apply_link", ""
        )
        company_site = job.get(
            "employer_website", ""
        )

        # Job title se skills guess karo
        title = job.get("job_title", "")
        description = job.get(
            "job_description", ""
        )[:500]

        # Common skills detect karo description se
        detected_skills = detect_skills_from_text(
            title + " " + description
        )

        # Salary format karo
        min_salary = job.get("job_min_salary")
        max_salary = job.get("job_max_salary")
        salary_period = job.get(
            "job_salary_period", ""
        )

        if min_salary and max_salary:
            # Convert to LPA if yearly
            if salary_period == "YEAR":
                min_lpa = round(min_salary / 100000, 1)
                max_lpa = round(max_salary / 100000, 1)
                salary = f"{min_lpa}-{max_lpa} LPA"
            else:
                salary = f"{min_salary}-{max_salary} {salary_period}"
        else:
            salary = "Not disclosed"

        # Job type
        employment_type = job.get(
            "job_employment_type", "FULLTIME"
        )
        job_type_map = {
            "FULLTIME": "Full Time",
            "PARTTIME": "Part Time",
            "INTERN": "Internship",
            "CONTRACTOR": "Contract"
        }
        job_type = job_type_map.get(
            employment_type, "Full Time"
        )

        # Remote check
        is_remote = job.get(
            "job_is_remote", False
        )

        # Location
        city = job.get("job_city", "")
        country = job.get("job_country", "India")
        location = f"{city}, {country}" if city else country

        # Apply date
        posted_at = job.get("job_posted_at_datetime_utc", "")
        apply_date = ""
        if posted_at:
            # 30 days add karo posted date mein
            try:
                from datetime import datetime, timedelta
                posted = datetime.fromisoformat(
                    posted_at.replace("Z", "+00:00")
                )
                deadline = posted + timedelta(days=30)
                apply_date = deadline.strftime("%Y-%m-%d")
            except Exception:
                apply_date = ""

        return {
            "id": hash(job.get("job_id", "")),
            "title": title,
            "company": job.get(
                "employer_name", "Unknown"
            ),
            "location": location,
            "salary": salary,
            "experience": "0-3 years",
            "remote": is_remote,
            "job_type": job_type,
            "description": description,
            "apply_date": apply_date,
            "required_skills": detected_skills,
            "good_to_have": [],
            "apply_links": {
                "linkedin": apply_link if "linkedin" in apply_link.lower() else "",
                "company": company_site or apply_link,
                "naukri": f"https://www.naukri.com/{title.lower().replace(' ', '-')}-jobs"
            },
            "source": "real",
            "job_id": job.get("job_id", "")
        }

    except Exception as e:
        print(f"Format error: {e}")
        return {}


# ------------------------------------------------
# FUNCTION 3 — detect_skills_from_text()
# ------------------------------------------------
# Job description se skills detect karo
# ------------------------------------------------

def detect_skills_from_text(text: str) -> List[str]:
    """
    Job title aur description se skills detect karo
    """
    text_lower = text.lower()

    # Skills dictionary
    skill_keywords = {
        "python": ["python"],
        "javascript": ["javascript", "js"],
        "react": ["react", "reactjs"],
        "nodejs": ["node.js", "nodejs", "node"],
        "machine learning": ["machine learning", "ml"],
        "deep learning": ["deep learning", "dl"],
        "tensorflow": ["tensorflow", "tf"],
        "pytorch": ["pytorch"],
        "docker": ["docker"],
        "kubernetes": ["kubernetes", "k8s"],
        "aws": ["aws", "amazon web services"],
        "sql": ["sql", "mysql", "postgresql"],
        "mongodb": ["mongodb", "mongo"],
        "git": ["git", "github"],
        "fastapi": ["fastapi"],
        "langchain": ["langchain"],
        "computer vision": ["computer vision", "opencv"],
        "nlp": ["nlp", "natural language"],
        "data science": ["data science"],
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "java": ["java"],
        "c++": ["c++", "cpp"],
        "typescript": ["typescript"],
        "redis": ["redis"],
        "kafka": ["kafka"],
        "spark": ["spark", "pyspark"]
    }

    detected = []
    for skill, keywords in skill_keywords.items():
        if any(kw in text_lower for kw in keywords):
            detected.append(skill)

    return detected[:8]