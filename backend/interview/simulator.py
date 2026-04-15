# ================================================
# simulator.py — AI Mock Interview Simulator
# ================================================
# YE FILE KYA KARTI HAI?
# 1. Interview questions generate karta hai
# 2. User ke answers evaluate karta hai
# 3. Detailed feedback deta hai
# 4. Multiple rounds support karta hai
#
# GROQ LLM use karta hai
# ================================================

from agents.career_agent import client
from config import settings
from typing import List, Dict, Optional
import json
import re


# ------------------------------------------------
# QUESTION BANK — Default Questions
# ------------------------------------------------
# Groq fail ho toh ye use hoga
# ------------------------------------------------

DEFAULT_QUESTIONS = {
    "technical": [
        {
            "id": 1,
            "question": "Explain the difference between supervised and unsupervised learning with examples.",
            "category": "Technical",
            "difficulty": "medium",
            "expected_points": [
                "Supervised: labeled data",
                "Unsupervised: unlabeled data",
                "Examples: Classification vs Clustering",
                "Real world applications"
            ]
        },
        {
            "id": 2,
            "question": "What is overfitting and how do you prevent it?",
            "category": "Technical",
            "difficulty": "medium",
            "expected_points": [
                "Definition of overfitting",
                "Train vs test performance gap",
                "Prevention: Regularization, Dropout",
                "Cross-validation"
            ]
        },
        {
            "id": 3,
            "question": "Explain how a neural network learns using backpropagation.",
            "category": "Technical",
            "difficulty": "hard",
            "expected_points": [
                "Forward pass",
                "Loss calculation",
                "Gradient descent",
                "Weight update"
            ]
        }
    ],
    "behavioral": [
        {
            "id": 4,
            "question": "Tell me about a challenging project you worked on. How did you handle it?",
            "category": "Behavioral",
            "difficulty": "medium",
            "expected_points": [
                "Situation clearly described",
                "Your specific role",
                "Steps taken (STAR format)",
                "Result/outcome"
            ]
        },
        {
            "id": 5,
            "question": "Describe a situation where you had to learn a new technology quickly.",
            "category": "Behavioral",
            "difficulty": "easy",
            "expected_points": [
                "Specific technology mentioned",
                "Learning approach",
                "Time taken",
                "How you applied it"
            ]
        }
    ],
    "hr": [
        {
            "id": 6,
            "question": "Tell me about yourself and your journey into tech.",
            "category": "HR",
            "difficulty": "easy",
            "expected_points": [
                "Brief background",
                "Technical skills highlight",
                "Key projects",
                "Career goals"
            ]
        },
        {
            "id": 7,
            "question": "Where do you see yourself in 5 years?",
            "category": "HR",
            "difficulty": "easy",
            "expected_points": [
                "Clear career vision",
                "Skill development plan",
                "Alignment with company",
                "Realistic goals"
            ]
        },
        {
            "id": 8,
            "question": "Why do you want to work in this role?",
            "category": "HR",
            "difficulty": "easy",
            "expected_points": [
                "Genuine interest shown",
                "Skills alignment",
                "Company research",
                "Career fit"
            ]
        }
    ]
}


# ------------------------------------------------
# FUNCTION 1 — generate_questions()
# ------------------------------------------------
# Role ke liye interview questions generate karo
# ------------------------------------------------

def generate_questions(
    role: str,
    skills: List[str],
    difficulty: str = "medium",
    num_questions: int = 5
) -> List[Dict]:
    """
    AI se interview questions generate karo

    Args:
        role: Job role (ML Engineer, SDE etc.)
        skills: User ki skills
        difficulty: easy/medium/hard
        num_questions: Kitne questions chahiye

    Returns:
        Questions list with metadata
    """

    skills_str = ", ".join(skills[:6]) if skills else role

    prompt = f"""Generate exactly {num_questions} interview questions 
for a {role} position.

Candidate's skills: {skills_str}
Difficulty level: {difficulty}

Return ONLY a valid JSON array (no extra text):
[
  {{
    "id": 1,
    "question": "Your question here",
    "category": "Technical",
    "difficulty": "{difficulty}",
    "expected_points": [
      "Key point 1 to look for",
      "Key point 2 to look for"
    ],
    "time_limit_seconds": 120,
    "hints": ["Hint 1", "Hint 2"]
  }}
]

Rules:
- Mix: 40% Technical, 30% Behavioral, 30% HR
- Technical questions should test {skills_str}
- Behavioral: Use STAR format scenarios
- HR: Career goals, motivation, culture fit
- Make questions relevant to Indian job market
- Generate EXACTLY {num_questions} questions"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )

        response_text = response.choices[0].message.content

        # JSON array extract karo
        json_match = re.search(
            r'\[.*\]',
            response_text,
            re.DOTALL
        )

        if json_match:
            questions = json.loads(json_match.group())
            print(f"✅ {len(questions)} questions generated by Groq!")
            return questions[:num_questions]

    except Exception as e:
        print(f"Question generation error: {e}")

    # Fallback questions use karo
    print("Using default questions...")
    return _get_default_questions(role, num_questions)


# ------------------------------------------------
# FUNCTION 2 — evaluate_answer()
# ------------------------------------------------
# User ka answer evaluate karo
# AI feedback do
# ------------------------------------------------

def evaluate_answer(
    question: str,
    user_answer: str,
    expected_points: List[str],
    role: str,
    category: str = "Technical"
) -> Dict:
    """
    User ka answer evaluate karo aur feedback do

    Args:
        question: Jo question poocha gaya
        user_answer: User ne jo answer diya
        expected_points: Kya points expect kiye the
        role: Job role
        category: Technical/Behavioral/HR

    Returns:
        Evaluation with score and feedback
    """

    # Empty answer check
    if not user_answer or len(user_answer.strip()) < 10:
        return {
            "score": 0,
            "out_of": 10,
            "grade": "F",
            "strengths": [],
            "improvements": [
                "Answer bahut short hai!",
                "Minimum 2-3 sentences mein explain karo",
                "Specific examples do"
            ],
            "ideal_answer_hint": (
                "Key points: " +
                ", ".join(expected_points[:3])
            ),
            "follow_up": "Can you elaborate on your answer?",
            "encouragement": "Practice karo — next time better karoge! 💪"
        }

    # Evaluation prompt
    prompt = f"""You are a senior {role} interviewer evaluating a candidate's answer.

Question: {question}

Expected Key Points:
{chr(10).join(f'- {p}' for p in expected_points)}

Candidate's Answer:
{user_answer}

Evaluate and return ONLY this JSON:
{{
  "score": 7,
  "out_of": 10,
  "grade": "B",
  "strengths": [
    "What was good about the answer"
  ],
  "improvements": [
    "What could be improved"
  ],
  "ideal_answer_hint": "Brief hint of what perfect answer includes",
  "follow_up": "A relevant follow-up question",
  "encouragement": "A motivating message for the candidate"
}}

Scoring guide:
9-10: Excellent - covered all points with examples
7-8: Good - covered most points
5-6: Average - covered some points
3-4: Below average - missed key points
1-2: Poor - very incomplete answer

Be constructive, encouraging, and specific.
Focus on Indian tech job market context."""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=800,
            temperature=0.5
        )

        response_text = response.choices[0].message.content

        # JSON extract karo
        json_match = re.search(
            r'\{.*\}',
            response_text,
            re.DOTALL
        )

        if json_match:
            evaluation = json.loads(json_match.group())
            print(f"✅ Answer evaluated! Score: {evaluation.get('score')}/10")
            return evaluation

    except Exception as e:
        print(f"Evaluation error: {e}")

    # Fallback evaluation
    return _fallback_evaluation(user_answer, expected_points)


# ------------------------------------------------
# FUNCTION 3 — calculate_interview_score()
# ------------------------------------------------
# Poore interview ka score calculate karo
# ------------------------------------------------

def calculate_interview_score(
    answers: List[Dict]
) -> Dict:
    """
    Saare answers ke basis pe
    Overall interview score calculate karo

    Args:
        answers: List of answered questions with evaluations

    Returns:
        Overall interview report
    """

    if not answers:
        return {
            "total_score": 0,
            "percentage": 0,
            "grade": "F",
            "verdict": "No answers submitted"
        }

    # Scores collect karo
    scores = []
    for answer in answers:
        evaluation = answer.get("evaluation", {})
        score = evaluation.get("score", 0)
        out_of = evaluation.get("out_of", 10)
        scores.append((score, out_of))

    # Total score calculate karo
    total_scored = sum(s[0] for s in scores)
    total_possible = sum(s[1] for s in scores)
    percentage = (total_scored / total_possible * 100) if total_possible > 0 else 0

    # Grade assign karo
    if percentage >= 85:
        grade = "A"
        verdict = "Excellent! You're ready to apply! 🌟"
    elif percentage >= 70:
        grade = "B"
        verdict = "Good performance! A bit more practice needed. 👍"
    elif percentage >= 55:
        grade = "C"
        verdict = "Average. Focus on weak areas. 📈"
    elif percentage >= 40:
        grade = "D"
        verdict = "Below average. More preparation needed. ⚠️"
    else:
        grade = "F"
        verdict = "Keep practicing! Don't give up! 💪"

    return {
        "total_score": round(total_scored, 1),
        "total_possible": total_possible,
        "percentage": round(percentage, 1),
        "grade": grade,
        "verdict": verdict,
        "questions_attempted": len(answers),
        "average_score": round(total_scored / len(answers), 1)
    }


# ------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------

def _get_default_questions(
    role: str,
    num_questions: int
) -> List[Dict]:
    """Default questions return karo"""

    all_questions = (
        DEFAULT_QUESTIONS["technical"] +
        DEFAULT_QUESTIONS["behavioral"] +
        DEFAULT_QUESTIONS["hr"]
    )

    # Role specific questions bhi add karo
    role_question = {
        "id": 9,
        "question": f"Explain your most significant project as a {role} candidate.",
        "category": "Technical",
        "difficulty": "medium",
        "expected_points": [
            "Project description",
            "Technology stack used",
            "Your specific contribution",
            "Challenges faced",
            "Results achieved"
        ],
        "time_limit_seconds": 180,
        "hints": [
            "Use STAR format",
            "Mention specific technologies",
            "Quantify results if possible"
        ]
    }

    all_questions.insert(0, role_question)
    return all_questions[:num_questions]


def _fallback_evaluation(
    answer: str,
    expected_points: List[str]
) -> Dict:
    """Fallback evaluation when AI fails"""

    # Simple scoring based on keywords
    answer_lower = answer.lower()
    points_covered = sum(
        1 for point in expected_points
        if any(
            word in answer_lower
            for word in point.lower().split()[:2]
        )
    )

    score = min(
        10,
        max(1, int(points_covered / len(expected_points) * 10))
    ) if expected_points else 5

    return {
        "score": score,
        "out_of": 10,
        "grade": "B" if score >= 7 else "C",
        "strengths": ["Answer diya — good start!"],
        "improvements": [
            "More specific examples add karo",
            "Technical depth increase karo"
        ],
        "ideal_answer_hint": (
            "Cover these points: " +
            ", ".join(expected_points[:3])
        ),
        "follow_up": "Can you elaborate more on your experience?",
        "encouragement": "Keep practicing! You're improving! 💪"
    }