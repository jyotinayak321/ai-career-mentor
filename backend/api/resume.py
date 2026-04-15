# ================================================
# resume.py — Resume Upload API
# ================================================
# YE FILE KYA KARTI HAI?
# 1. Resume file accept karta hai (PDF/DOCX)
# 2. Text extract karta hai
# 3. Skills, education parse karta hai
# 4. Score calculate karta hai
# 5. Database mein save karta hai
# 6. Complete analysis return karta hai
#
# ENDPOINT:
# POST /api/resume/upload
# GET  /api/resume/history
# ================================================

from fastapi import (
    APIRouter,
    UploadFile,    # File upload ke liye
    File,          # File parameter ke liye
    Depends,       # Dependency injection
    HTTPException  # Error handling
)
from api.auth import get_current_user #auth.py se user authentication ke liye function import karo 
from resume_parser.parser import parse_resume #resume_parser/parser.py se resume parsing ke liye function import karo
from resume_parser.scorer import score_resume # resume_parser/scorer.py se resume scoring ke liye function import karo
from database.mongodb import get_db # database/mongodb.py se MongoDB connection ke liye function import karo
import datetime

# Router banao
router = APIRouter()


# ------------------------------------------------
# ROUTE 1 — UPLOAD RESUME
# ------------------------------------------------
# POST /api/resume/upload
#
# FLOW:
# 1. User token bhejta hai (Authorization)
# 2. User file attach karta hai
# 3. Hum file validate karte hain
# 4. Parse karte hain
# 5. Score karte hain
# 6. Save karte hain
# 7. Result return karte hain
# ------------------------------------------------

@router.post("/upload") 
async def upload_resume(
    # UploadFile = FastAPI ka file handler
    # File(...) = Required field hai
    file: UploadFile = File(...),
    
    # Depends = Dependency injection
    # get_current_user automatically:
    # 1. Token check karega
    # 2. User dhundega
    # 3. User return karega
    # Agar token invalid = 401 Error!
    current_user: dict = Depends(get_current_user) # current_user variable mein authenticated user ki information milegi
):
    """
    Resume upload karo aur analysis lo
    
    Headers mein chahiye:
    Authorization: Bearer <token>
    
    Form data mein chahiye:
    file: PDF ya DOCX file
    """
    
    # ----------------------------------------
    # STEP 1 — FILE VALIDATE KARO
    # ----------------------------------------
    # Sirf PDF aur DOCX allow hai
    # Koi bhi random file nahi!
    
    filename = file.filename
    
    # File extension check karo
    if not (
        filename.endswith('.pdf') or
        filename.endswith('.docx') or
        filename.endswith('.txt')
    ):
        raise HTTPException(  # HTTPException raise karte hain agar file valid nahi hai
            status_code=400,
            detail="Sirf PDF ya DOCX files allowed hain!"
        )
    
    # ----------------------------------------
    # STEP 2 — FILE BYTES READ KARO
    # ----------------------------------------
    # await file.read() = File ka content lo
    # bytes format mein milega
    
    file_bytes = await file.read()
    
    # File size check karo (max 5MB)
    # 5 * 1024 * 1024 = 5,242,880 bytes = 5MB
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File 5MB se badi nahi honi chahiye!"
        )
    
    # ----------------------------------------
    # STEP 3 — RESUME PARSE KARO
    # ----------------------------------------
    # parser.py ka parse_resume() call karo
    # Skills, education, experience nikalo
    
    try:
        parsed_data = parse_resume(file_bytes, filename)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File process nahi ho saki: {str(e)}"
        )
    
    # ----------------------------------------
    # STEP 4 — SCORE CALCULATE KARO
    # ----------------------------------------
    # scorer.py ka score_resume() call karo
    
    score_result = score_resume(parsed_data)
    
    # ----------------------------------------
    # STEP 5 — DATABASE MEIN SAVE KARO
    # ----------------------------------------
    
    db = get_db()
    
    # Resume document banao
    resume_doc = {
        # Kaun sa user hai
        "user_id": str(current_user["_id"]),
        
        # File ka naam
        "filename": filename,
        
        # Parse hua data
        "parsed_data": parsed_data,
        
        # Score information
        "score": score_result["score"],
        "grade": score_result["grade"],
        "feedback": score_result["feedback"],
        
        # Kab upload kiya
        "uploaded_at": datetime.datetime.utcnow()
    }
    
    # MongoDB mein save karo
    await db.resumes.insert_one(resume_doc)
    
    # User ki skills update karo
    # $set = Field update karo
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {
            "skills": parsed_data["skills"],
            "resume_score": score_result["score"]
        }}
    )
    
    # ----------------------------------------
    # STEP 6 — RESULT RETURN KARO
    # ----------------------------------------
    
    return {
        "message": "Resume successfully analyzed! 🎉",
        
        # Parse ki gayi information
        "parsed_info": {
            "email": parsed_data["email"],
            "phone": parsed_data["phone"],
            "skills_found": parsed_data["skills"],
            "skills_count": parsed_data["skills_count"],
            "education": parsed_data["education"],
            "experience": parsed_data["experience"]
        },
        
        # Score report
        "score_report": {
            "score": score_result["score"],
            "grade": score_result["grade"],
            "grade_label": score_result["grade_label"],
            "breakdown": score_result["breakdown"],
            "feedback": score_result["feedback"]
        }
    }


# ------------------------------------------------
# ROUTE 2 — RESUME HISTORY
# ------------------------------------------------
# GET /api/resume/history
#
# User ki saari previous uploads dikhao
# ------------------------------------------------

@router.get("/history") # GET request for resume history
async def get_resume_history(
    current_user: dict = Depends(get_current_user)
):
    """
    User ki resume upload history lo
    """
    db = get_db()
    
    # User ki saari resumes dhundo
    # sort = Latest pehle
    # to_list(10) = Maximum 10 results
    resumes = await db.resumes.find(
        {"user_id": str(current_user["_id"])}
    ).sort(
        "uploaded_at", -1  # -1 = Descending (latest first)
    ).to_list(10)
    
    # MongoDB _id convert karo
    # _id directly serialize nahi hota!
    for resume in resumes:
        resume["_id"] = str(resume["_id"])
    
    return {
        "total": len(resumes),
        "resumes": resumes
    }