# ================================================
# scorer.py — Resume Scoring System
# ================================================
# YE FILE KYA KARTI HAI?
# Resume ko 100 mein se score deti hai
# Aur improvement feedback deti hai
#
# SCORING CRITERIA:
# Skills     → 40 points
# Education  → 20 points
# Experience → 20 points
# Contact    → 20 points
# Total      → 100 points
# ================================================

from typing import Dict, List


def score_resume(parsed_data: Dict) -> Dict:
    """
    Resume score karo
    
    Args:
        parsed_data: parser.py ka output
    
    Returns:
        score, grade, feedback dictionary
    """
    
    score = 0
    feedback = []
    breakdown = {}
    
    # ----------------------------------------
    # CRITERIA 1 — SKILLS (40 points)
    # ----------------------------------------
    # Jitni zyada skills = Zyada points
    #
    # 15+ skills = 40 points (Full marks)
    # 10-14      = 30 points
    # 5-9        = 20 points
    # 1-4        = 10 points
    # 0          = 0 points
    # ----------------------------------------
    
    skills = parsed_data.get("skills", [])
    skills_count = len(skills)
    
    if skills_count >= 15:
        skills_score = 40
        # Koi feedback nahi — perfect!
    elif skills_count >= 10:
        skills_score = 30
        feedback.append(
            "💡 Aur skills add karo — "
            f"abhi {skills_count} hain, "
            "15+ honi chahiye"
        )
    elif skills_count >= 5:
        skills_score = 20
        feedback.append(
            f"⚠️ Sirf {skills_count} skills mili — "
            "Skills section improve karo"
        )
    elif skills_count > 0:
        skills_score = 10
        feedback.append(
            "❌ Bahut kam skills hain — "
            "Technical skills zaroor likho"
        )
    else:
        skills_score = 0
        feedback.append(
            "❌ Koi bhi skills nahi mili — "
            "Skills section add karo!"
        )
    
    score += skills_score
    breakdown["skills"] = skills_score
    
    # ----------------------------------------
    # CRITERIA 2 — EDUCATION (20 points)
    # ----------------------------------------
    
    education = parsed_data.get("education", [])
    edu_count = len(education)
    
    if edu_count >= 2:
        edu_score = 20
    elif edu_count == 1:
        edu_score = 12
        feedback.append(
            "💡 Education section mein "
            "aur details add karo"
        )
    else:
        edu_score = 0
        feedback.append(
            "❌ Education section nahi mila"
        )
    
    score += edu_score
    breakdown["education"] = edu_score
    
    # ----------------------------------------
    # CRITERIA 3 — EXPERIENCE (20 points)
    # ----------------------------------------
    
    experience = parsed_data.get("experience", [])
    exp_count = len(experience)
    
    if exp_count >= 3:
        exp_score = 20
    elif exp_count >= 1:
        exp_score = 12
        feedback.append(
            "💡 Internships aur projects "
            "experience section mein likho"
        )
    else:
        exp_score = 0
        feedback.append(
            "⚠️ Experience section nahi mila — "
            "Projects ya internships add karo"
        )
    
    score += exp_score
    breakdown["experience"] = exp_score
    
    # ----------------------------------------
    # CRITERIA 4 — CONTACT INFO (20 points)
    # ----------------------------------------
    
    contact_score = 0
    
    if parsed_data.get("email"):
        contact_score += 10
    else:
        feedback.append("❌ Email ID nahi mili")
    
    if parsed_data.get("phone"):
        contact_score += 10
    else:
        feedback.append("❌ Phone number nahi mila")
    
    score += contact_score
    breakdown["contact"] = contact_score
    
    # ----------------------------------------
    # GENERAL FEEDBACK
    # ----------------------------------------
    
    if score < 70:
        feedback.append(
            "💡 GitHub profile ka link add karo"
        )
        feedback.append(
            "💡 Action verbs use karo: "
            "Built, Developed, Implemented"
        )
        feedback.append(
            "💡 Projects section mein "
            "tech stack clearly likho"
        )
    
    # ----------------------------------------
    # GRADE ASSIGN KARO
    # ----------------------------------------
    #
    # Score → Grade → Label
    # 85+   →   A   → Excellent
    # 70-84 →   B   → Good
    # 55-69 →   C   → Average
    # 40-54 →   D   → Below Average
    # <40   →   F   → Needs Improvement
    # ----------------------------------------
    
    if score >= 85:
        grade = "A"
        grade_label = "Excellent! 🌟"
    elif score >= 70:
        grade = "B"
        grade_label = "Good! 👍"
    elif score >= 55:
        grade = "C"
        grade_label = "Average 📈"
    elif score >= 40:
        grade = "D"
        grade_label = "Below Average ⚠️"
    else:
        grade = "F"
        grade_label = "Needs Improvement ❌"
    
    return {
        "score": score,
        "grade": grade,
        "grade_label": grade_label,
        "breakdown": breakdown,
        "feedback": feedback,
        "total_skills": skills_count
    }