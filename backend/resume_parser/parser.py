# ================================================
# parser.py — Resume Parser Module
# ================================================
# YE FILE KYA KARTI HAI?
# Resume PDF/DOCX/TXT se information nikaalti hai
#
# KAISE KAAM KARTA HAI?
# Step 1: File type dekho
# Step 2: Text nikalo
# Step 3: Email, phone nikalo (regex)
# Step 4: Skills nikalo (keyword matching)
# Step 5: Education, experience nikalo
# Step 6: Structured data return karo
# ================================================

# re = Regular Expressions
# Pattern matching ke liye
import re

from typing import List, Dict


# ------------------------------------------------
# SKILLS DATABASE
# ------------------------------------------------
# Ye hamare known skills hain
# Resume mein in skills ko dhundenge
# ------------------------------------------------

TECH_SKILLS = {
    "programming": [
        "python", "java", "javascript",
        "c++", "c#", "typescript", "go",
        "rust", "kotlin", "swift", "php",
        "ruby", "scala", "r", "matlab"
    ],
    "web": [
        "react", "angular", "vue", "html",
        "css", "nodejs", "django", "flask",
        "fastapi", "express", "nextjs",
        "tailwind", "bootstrap", "jquery"
    ],
    "ai_ml": [
        "machine learning", "deep learning",
        "nlp", "computer vision", "tensorflow",
        "pytorch", "scikit-learn", "keras",
        "langchain", "huggingface", "pandas",
        "numpy", "matplotlib", "seaborn",
        "rag", "llm", "generative ai"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb",
        "redis", "sqlite", "oracle",
        "firebase", "chromadb", "faiss",
        "sql", "nosql"
    ],
    "cloud": [
        "aws", "azure", "gcp", "docker",
        "kubernetes", "terraform", "jenkins",
        "github actions", "ci/cd", "linux"
    ],
    "tools": [
        "git", "github", "postman", "jira",
        "figma", "tableau", "power bi",
        "excel", "vs code"
    ]
}

# Saari skills ek flat set mein
ALL_SKILLS = set()
for category_skills in TECH_SKILLS.values():
    ALL_SKILLS.update(category_skills)


# ------------------------------------------------
# FUNCTION 1 — extract_text_from_pdf()
# ------------------------------------------------

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """PDF bytes se text extract karo"""
    import pdfplumber
    import io

    text = ""

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()


# ------------------------------------------------
# FUNCTION 2 — extract_text_from_docx()
# ------------------------------------------------

def extract_text_from_docx(file_bytes: bytes) -> str:
    """DOCX bytes se text extract karo"""
    from docx import Document
    import io

    doc = Document(io.BytesIO(file_bytes))
    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text.strip()


# ------------------------------------------------
# FUNCTION 3 — extract_email()
# ------------------------------------------------

def extract_email(text: str) -> str:
    """
    Text se email nikalo
    
    Regex pattern:
    [A-Za-z0-9._%+-]+ = Email start
    @                  = At symbol
    [A-Za-z0-9.-]+     = Domain
    [A-Z|a-z]{2,}      = Extension
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""


# ------------------------------------------------
# FUNCTION 4 — extract_phone()
# ------------------------------------------------

def extract_phone(text: str) -> str:
    """
    Text se Indian phone number nikalo
    
    Fix kiya:
    Pehle "Phone:" prefix hatao
    Phir number dhundo
    """
    # Multiple patterns try karo
    patterns = [
        # +91 ke saath
        r'\+91[\s\-]?[6-9]\d{9}',
        # 0 se shuru
        r'0[6-9]\d{9}',
        # Simple 10 digit
        r'[6-9]\d{9}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Sirf digits return karo
            phone = re.sub(r'\D', '', matches[0])
            # 10 digits hone chahiye
            if len(phone) == 10:
                return phone
            elif len(phone) == 12:
                # +91 included hai
                return phone[2:]
    
    return ""


# ------------------------------------------------
# FUNCTION 5 — extract_skills()
# ------------------------------------------------

def extract_skills(text: str) -> List[str]:
    """
    Text se technical skills nikalo
    
    Kaise kaam karta hai:
    1. Text lowercase karo
    2. Har known skill check karo
    3. Word boundary match karo
    4. Mili skills return karo
    """
    text_lower = text.lower()
    found_skills = []

    for skill in ALL_SKILLS:
        # Word boundary check
        # "java" != "javascript"
        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(found_skills)


# ------------------------------------------------
# FUNCTION 6 — extract_education()
# ------------------------------------------------

def extract_education(text: str) -> List[str]:
    """Text se education details nikalo"""
    education = []

    # Degree patterns dhundo
    degree_patterns = [
        r'B[.\s]?Tech[^\n]*',
        r'Bachelor[^\n]*',
        r'B[.\s]?E[^\n]*',
        r'M[.\s]?Tech[^\n]*',
        r'Master[^\n]*',
        r'MBA[^\n]*',
        r'Ph[.\s]?D[^\n]*',
        r'12th[^\n]*',
        r'10th[^\n]*',
        r'Intermediate[^\n]*',
        r'Graduation[^\n]*',
        r'CGPA[^\n]*',
        r'GPA[^\n]*'
    ]

    for pattern in degree_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )
        for match in matches:
            clean = match.strip()
            if len(clean) > 5 and clean not in education:
                education.append(clean[:100])

    return education[:5]


# ------------------------------------------------
# FUNCTION 7 — extract_experience()
# ------------------------------------------------

def extract_experience(text: str) -> List[str]:
    """Text se experience details nikalo"""
    experience = []

    # Experience keywords
    exp_keywords = [
        'internship', 'intern', 'engineer',
        'developer', 'analyst', 'worked',
        'experience', 'trainee', 'associate',
        'built', 'developed', 'created',
        'designed', 'implemented'
    ]

    lines = text.split('\n')

    for line in lines:
        line_lower = line.lower()
        line_clean = line.strip()

        if any(kw in line_lower for kw in exp_keywords):
            if len(line_clean) > 20:
                experience.append(line_clean[:150])

    return experience[:8]


# ------------------------------------------------
# MAIN FUNCTION — parse_resume()
# ------------------------------------------------
# Ye sabhi functions ko call karta hai
# Complete parsed result return karta hai
# ------------------------------------------------

def parse_resume(
    file_bytes: bytes,
    filename: str
) -> Dict:
    """
    Resume parse karo aur structured data lo

    Args:
        file_bytes: File ka binary data
        filename: File ka naam

    Returns:
        Dictionary with all extracted info
    """

    filename_lower = filename.lower()

    # ----------------------------------------
    # FILE TYPE SE TEXT NIKALO
    # ----------------------------------------

    if filename_lower.endswith('.pdf'):
        # PDF se text nikalo
        text = extract_text_from_pdf(file_bytes)

    elif filename_lower.endswith('.docx'):
        # DOCX se text nikalo
        text = extract_text_from_docx(file_bytes)

    elif filename_lower.endswith('.txt'):
        # TXT file directly decode karo
        # UTF-8 = Standard text encoding
        # errors='ignore' = Koi bhi
        # invalid character ignore karo
        text = file_bytes.decode(
            'utf-8',
            errors='ignore'
        )

    else:
        # Unsupported format
        raise ValueError(
            f"Unsupported format: {filename}\n"
            "Sirf PDF, DOCX ya TXT allowed hai!"
        )

    # ----------------------------------------
    # TEXT VALIDATE KARO
    # ----------------------------------------

    if len(text) < 50:
        raise ValueError(
            "Resume mein bahut kam text hai!\n"
            "Sahi file upload karo."
        )

    # ----------------------------------------
    # SARI INFORMATION EXTRACT KARO
    # ----------------------------------------

    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    # ----------------------------------------
    # STRUCTURED RESULT RETURN KARO
    # ----------------------------------------

    return {
        "email": email,
        "phone": phone,
        "skills": skills,
        "skills_count": len(skills),
        "education": education,
        "experience": experience,
        "raw_text_preview": text[:300] + "..."
    }