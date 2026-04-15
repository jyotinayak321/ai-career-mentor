# ================================================
# detector.py — Skill Gap Detection Module
# ================================================
# YE FILE KYA KARTI HAI?
# User ki skills compare karti hai
# Industry requirements se
# Aur gap report generate karti hai
#
# ANALOGY:
# Ek checklist hai job ke liye
# Tumhari skills checklist pe lagao
# Jo nahi lagi = Skill Gap!
# ================================================

from typing import List, Dict


# ------------------------------------------------
# INDUSTRY REQUIREMENTS DATABASE
# ------------------------------------------------
# Har role ke liye required skills
# 3 levels mein divide kiya:
#
# essential    = Must have (job nahi milegi bina)
# important    = Should have (competitive edge)
# good_to_have = Nice to have (bonus points)
# ------------------------------------------------

ROLE_REQUIREMENTS = {

    "software engineer": {
        "essential": [
            "python", "data structures",
            "algorithms", "git", "sql",
            "problem solving"
        ],
        "important": [
            "javascript", "react", "nodejs",
            "docker", "aws", "system design",
            "rest api"
        ],
        "good_to_have": [
            "kubernetes", "redis", "graphql",
            "typescript", "ci/cd", "mongodb"
        ]
    },

    "ml engineer": {
        "essential": [
            "python", "machine learning",
            "deep learning", "mathematics",
            "statistics", "git"
        ],
        "important": [
            "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy",
            "docker", "sql", "langchain"
        ],
        "good_to_have": [
            "aws", "mlops", "kubernetes",
            "spark", "airflow", "wandb",
            "rag", "llm"
        ]
    },

    "data scientist": {
        "essential": [
            "python", "statistics",
            "machine learning", "pandas",
            "numpy", "sql"
        ],
        "important": [
            "matplotlib", "seaborn",
            "scikit-learn", "deep learning",
            "tableau", "git", "excel"
        ],
        "good_to_have": [
            "spark", "airflow", "aws",
            "tensorflow", "r", "power bi"
        ]
    },

    "frontend developer": {
        "essential": [
            "javascript", "react", "html",
            "css", "git"
        ],
        "important": [
            "typescript", "nodejs", "tailwind",
            "nextjs", "rest api", "responsive design"
        ],
        "good_to_have": [
            "graphql", "webpack", "docker",
            "figma", "vue", "testing"
        ]
    },

    "backend developer": {
        "essential": [
            "python", "sql", "rest api",
            "git", "databases"
        ],
        "important": [
            "fastapi", "docker", "mongodb",
            "postgresql", "redis", "aws"
        ],
        "good_to_have": [
            "kubernetes", "kafka",
            "elasticsearch", "grpc",
            "terraform", "microservices"
        ]
    },

    "devops engineer": {
        "essential": [
            "docker", "kubernetes", "linux",
            "git", "ci/cd"
        ],
        "important": [
            "aws", "terraform", "jenkins",
            "ansible", "monitoring", "bash"
        ],
        "good_to_have": [
            "azure", "gcp", "prometheus",
            "grafana", "helm", "python"
        ]
    }
}

# Learning resources database
# Har skill ke liye best resources
LEARNING_RESOURCES = {
    "python": {
        "platform": "freeCodeCamp",
        "url": "https://freecodecamp.org",
        "duration": "2-3 months",
        "free": True
    },
    "machine learning": {
        "platform": "Coursera — Andrew Ng",
        "url": "https://coursera.org/learn/machine-learning",
        "duration": "3-4 months",
        "free": False
    },
    "deep learning": {
        "platform": "Fast.ai",
        "url": "https://fast.ai",
        "duration": "2-3 months",
        "free": True
    },
    "docker": {
        "platform": "Docker Official Docs",
        "url": "https://docs.docker.com",
        "duration": "2-4 weeks",
        "free": True
    },
    "aws": {
        "platform": "AWS Free Tier",
        "url": "https://aws.amazon.com/free",
        "duration": "2-3 months",
        "free": True
    },
    "react": {
        "platform": "React Official Docs",
        "url": "https://react.dev",
        "duration": "1-2 months",
        "free": True
    },
    "system design": {
        "platform": "Grokking System Design",
        "url": "https://educative.io",
        "duration": "2-3 months",
        "free": False
    },
    "data structures": {
        "platform": "LeetCode",
        "url": "https://leetcode.com",
        "duration": "3-6 months",
        "free": True
    },
    "kubernetes": {
        "platform": "Kubernetes Docs",
        "url": "https://kubernetes.io/docs",
        "duration": "1-2 months",
        "free": True
    },
    "langchain": {
        "platform": "LangChain Docs",
        "url": "https://python.langchain.com",
        "duration": "2-4 weeks",
        "free": True
    }
}


# ------------------------------------------------
# FUNCTION 1 — find_matching_role()
# ------------------------------------------------
# User ke target role ko
# hamare database se match karo
# ------------------------------------------------

def find_matching_role(target_role: str) -> str:
    """
    Target role ko database mein dhundo

    Kaise kaam karta hai:
    User ne likha: "ML Engineer"
    Database mein: "ml engineer"

    Lowercase karke compare karo
    Partial match bhi allow karo
    """
    target_lower = target_role.lower().strip()

    # Exact match dhundo
    if target_lower in ROLE_REQUIREMENTS:
        return target_lower

    # Partial match dhundo
    # "machine learning engineer" → "ml engineer"
    for role in ROLE_REQUIREMENTS.keys():
        if role in target_lower:
            return role
        if target_lower in role:
            return role

    # Keyword based match
    # "AI Engineer" → "ml engineer"
    keyword_map = {
        "ml": "ml engineer",
        "ai": "ml engineer",
        "machine learning": "ml engineer",
        "data": "data scientist",
        "frontend": "frontend developer",
        "front end": "frontend developer",
        "backend": "backend developer",
        "back end": "backend developer",
        "devops": "devops engineer",
        "software": "software engineer",
        "sde": "software engineer",
        "swe": "software engineer",
        "full stack": "software engineer"
    }

    for keyword, role in keyword_map.items():
        if keyword in target_lower:
            return role

    # Default role return karo
    return "software engineer"


# ------------------------------------------------
# FUNCTION 2 — calculate_match()
# ------------------------------------------------
# User skills aur required skills
# match percentage calculate karo
# ------------------------------------------------

def calculate_match(
    user_skills: List[str],
    required_skills: List[str]
) -> float:
    """
    Match percentage calculate karo

    Formula:
    matched / total_required * 100

    Example:
    Required: [python, docker, aws, sql] = 4
    User has: [python, sql] = 2 matched
    Match = 2/4 * 100 = 50%
    """
    if not required_skills:
        return 0.0

    user_set = set(s.lower() for s in user_skills)
    required_set = set(
        s.lower() for s in required_skills
    )

    # Intersection = Common skills
    matched = user_set & required_set

    match_percentage = (
        len(matched) / len(required_set)
    ) * 100

    return round(match_percentage, 1)


# ------------------------------------------------
# FUNCTION 3 — get_readiness_level()
# ------------------------------------------------
# Match percentage se readiness level
# ------------------------------------------------

def get_readiness_level(percentage: float) -> str:
    """
    Match percentage se readiness level lo

    80%+ = Job Ready
    60%+ = Almost Ready
    40%+ = In Progress
    20%+ = Early Stage
    <20% = Beginner
    """
    if percentage >= 80:
        return "Job Ready! 🟢"
    elif percentage >= 60:
        return "Almost Ready 🟡"
    elif percentage >= 40:
        return "In Progress 🟠"
    elif percentage >= 20:
        return "Early Stage 🔴"
    else:
        return "Beginner — Start karo! ⚪"


# ------------------------------------------------
# FUNCTION 4 — get_resources()
# ------------------------------------------------
# Missing skills ke liye resources suggest karo
# ------------------------------------------------

def get_resources(skills: List[str]) -> List[Dict]:
    """
    Skills ke liye learning resources lo
    """
    resources = []

    for skill in skills[:5]:
        # Skill ke liye resource dhundo
        skill_lower = skill.lower()

        if skill_lower in LEARNING_RESOURCES:
            resource = LEARNING_RESOURCES[skill_lower]
            resources.append({
                "skill": skill,
                "platform": resource["platform"],
                "url": resource["url"],
                "duration": resource["duration"],
                "free": resource["free"]
            })
        else:
            # Generic resource
            resources.append({
                "skill": skill,
                "platform": "YouTube + Documentation",
                "url": f"https://youtube.com/search?q={skill}+tutorial",
                "duration": "2-4 weeks",
                "free": True
            })

    return resources


# ------------------------------------------------
# MAIN FUNCTION — detect_skill_gap()
# ------------------------------------------------
# Ye sabhi functions call karta hai
# Complete gap report return karta hai
# ------------------------------------------------

def detect_skill_gap(
    user_skills: List[str],
    target_role: str = "software engineer"
) -> Dict:
    """
    Skill gap detect karo aur report banao

    Args:
        user_skills: Resume se nikali skills
        target_role: Jis role ke liye apply karna

    Returns:
        Complete gap analysis report
    """

    # ----------------------------------------
    # STEP 1 — Role match karo
    # ----------------------------------------
    matched_role = find_matching_role(target_role)
    requirements = ROLE_REQUIREMENTS[matched_role]

    # ----------------------------------------
    # STEP 2 — User skills lowercase karo
    # ----------------------------------------
    user_skills_lower = [
        s.lower() for s in user_skills
    ]
    user_set = set(user_skills_lower)

    # ----------------------------------------
    # STEP 3 — Missing skills find karo
    # ----------------------------------------

    # Essential mein se missing
    missing_essential = [
        skill for skill in requirements["essential"]
        if skill not in user_set
    ]

    # Important mein se missing
    missing_important = [
        skill for skill in requirements["important"]
        if skill not in user_set
    ]

    # Good to have mein se missing
    missing_good = [
        skill for skill in requirements["good_to_have"]
        if skill not in user_set
    ]

    # ----------------------------------------
    # STEP 4 — Matched skills find karo
    # ----------------------------------------

    all_required = (
        requirements["essential"] +
        requirements["important"]
    )

    matched_skills = [
        skill for skill in all_required
        if skill in user_set
    ]

    # ----------------------------------------
    # STEP 5 — Match percentage calculate
    # ----------------------------------------

    # Essential + Important ka match
    match_percentage = calculate_match(
        user_skills,
        requirements["essential"] +
        requirements["important"]
    )

    # ----------------------------------------
    # STEP 6 — Recommendations banao
    # ----------------------------------------

    recommendations = []

    # High priority — Essential missing
    if missing_essential:
        recommendations.append({
            "priority": "HIGH 🔴",
            "message": (
                f"Ye essential skills seekho pehle: "
                f"{', '.join(missing_essential[:3])}"
            ),
            "skills": missing_essential,
            "resources": get_resources(
                missing_essential
            )
        })

    # Medium priority — Important missing
    if missing_important:
        recommendations.append({
            "priority": "MEDIUM 🟡",
            "message": (
                f"Ye important skills add karo: "
                f"{', '.join(missing_important[:3])}"
            ),
            "skills": missing_important,
            "resources": get_resources(
                missing_important
            )
        })

    # Low priority — Good to have missing
    if missing_good:
        recommendations.append({
            "priority": "LOW 🟢",
            "message": (
                f"Bonus skills for edge: "
                f"{', '.join(missing_good[:3])}"
            ),
            "skills": missing_good,
            "resources": []
        })

    # ----------------------------------------
    # STEP 7 — Complete report return karo
    # ----------------------------------------

    return {
        # Role information
        "target_role": matched_role,
        "original_query": target_role,

        # Match statistics
        "match_percentage": match_percentage,
        "readiness_level": get_readiness_level(
            match_percentage
        ),

        # Skills analysis
        "matched_skills": matched_skills,
        "total_matched": len(matched_skills),

        # Gap analysis
        "gap_analysis": {
            "missing_essential": missing_essential,
            "missing_important": missing_important,
            "missing_good_to_have": missing_good,
            "total_missing": (
                len(missing_essential) +
                len(missing_important)
            )
        },

        # Action plan
        "recommendations": recommendations,

        # Summary message
        "summary": _generate_summary(
            matched_role,
            match_percentage,
            missing_essential
        )
    }


# ------------------------------------------------
# HELPER — _generate_summary()
# ------------------------------------------------

def _generate_summary(
    role: str,
    match: float,
    missing_essential: List[str]
) -> str:
    """
    Human readable summary generate karo
    """
    if match >= 80:
        return (
            f"Tum {role} ke liye almost ready ho! "
            f"Bas kuch polish karo aur apply karo!"
        )
    elif match >= 60:
        return (
            f"Acchi progress! {role} ke liye "
            f"kuch aur skills chahiye. "
            f"Focus karo: "
            f"{', '.join(missing_essential[:2])}"
        )
    elif match >= 40:
        return (
            f"{role} ke liye journey shuru hai! "
            f"Pehle ye seekho: "
            f"{', '.join(missing_essential[:3])}"
        )
    else:
        return (
            f"{role} ke liye foundation banana hai. "
            f"Basics se shuru karo!"
        )