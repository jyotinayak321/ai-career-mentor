# ================================================
# auth.py
# ================================================
# YE FILE KYA KARTI HAI?
# 1. User Register karta hai
# 2. User Login karta hai
# 3. Current user identify karta hai
#
# ENDPOINTS:
# POST /api/auth/register → Naya account
# POST /api/auth/login    → Login karo
# ================================================

from fastapi import APIRouter, HTTPException, Depends 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database.mongodb import get_db
from utils.jwt_handler import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)
import datetime

# ------------------------------------------------
# ROUTER BANAO
# ------------------------------------------------
# Router = Mini FastAPI app
# Ek group of related routes
#
# main.py mein register hoga:
# app.include_router(router,
#     prefix="/api/auth")
#
# Matlab sab routes /api/auth se
# shuru honge automatically!
# ------------------------------------------------

router = APIRouter()

# HTTPBearer = Authorization header se
# token extract karne ke liye
security = HTTPBearer()

# ------------------------------------------------
# PYDANTIC MODELS
# ------------------------------------------------
# Pydantic = Data validation library
# BaseModel = Base class for all models
#
# Ye models define karte hain:
# Request mein kya data aana chahiye
# Kaunsa field required hai
# Kaunsa type hona chahiye
#
# Agar wrong data aaya toh
# FastAPI automatically error deta hai!
# ------------------------------------------------

# Register ke liye data model
class UserRegister(BaseModel):
    # str = String hona chahiye
    name: str           # "Jyoti Nayak"
    # EmailStr = Valid email format
    # "jyoti" → Error ❌
    # "jyoti@gmail.com" → OK ✅
    email: str     # "jyoti@gmail.com"
    password: str       # "mypassword123"

# Login ke liye data model
class UserLogin(BaseModel):
    email:str     # "jyoti@gmail.com"
    password: str       # "mypassword123"


# ------------------------------------------------
# ROUTE 1 — REGISTER
# ------------------------------------------------
# POST /api/auth/register
#
# Kya karta hai?
# 1. Email already exist karta hai check karo
# 2. Password hash karo
# 3. Database mein save karo
# 4. JWT token banao
# 5. Token return karo
# ------------------------------------------------

@router.post("/register")
async def register(user_data: UserRegister):
    
    # Database object lo
    db = get_db()

    # ----------------------------------------
    # CHECK — Email already exist karta hai?
    # ----------------------------------------
    # find_one() = Ek document dhundo
    # {"email": user_data.email} = Filter
    # Matlab: Is email se koi user hai?
    
    existing_user = await db.users.find_one(
        {"email": user_data.email}
    )

    # Agar user mila toh error do
    if existing_user:
        # HTTPException = HTTP Error
        # status_code=400 = Bad Request
        # detail = Error message
        raise HTTPException(
            status_code=400,
            detail="Email already registered hai!"
        )

    # ----------------------------------------
    # PASSWORD HASH KARO
    # ----------------------------------------
    # Kabhi plain password store mat karo!
    # "jyoti123" → "$2b$12$xK9..."
    hashed_pw = hash_password(user_data.password)

    # ----------------------------------------
    # USER DOCUMENT BANAO
    # ----------------------------------------
    # MongoDB mein JSON document store hota hai
    # Ye sara data ek user ke liye store hoga
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_pw,      # Hashed! ✅
        "skills": [],               # Baad mein bharega
        "resume_score": 0,          # Baad mein update hoga
        "target_role": "",          # Baad mein set hoga
        "created_at": datetime.datetime.utcnow()
    }

    # ----------------------------------------
    # DATABASE MEIN SAVE KARO
    # ----------------------------------------
    # insert_one() = Ek document insert karo
    # result.inserted_id = Naya ID milega
    result = await db.users.insert_one(user_doc)

    # ----------------------------------------
    # JWT TOKEN BANAO
    # ----------------------------------------
    # Ab user registered hai
    # Token banao taaki seedha logged in ho
    
    token = create_access_token({
        "sub": user_data.email,
        "user_id": str(result.inserted_id)
    })

    # ----------------------------------------
    # RESPONSE RETURN KARO
    # ----------------------------------------
    return {
        "message": "Registration successful! 🎉",
        "token": token,
        "user": {
            "name": user_data.name,
            "email": user_data.email
        }
    }


# ------------------------------------------------
# ROUTE 2 — LOGIN
# ------------------------------------------------
# POST /api/auth/login
#
# Kya karta hai?
# 1. Email se user dhundo
# 2. Password verify karo
# 3. JWT token banao
# 4. Token return karo
# ------------------------------------------------

@router.post("/login")
async def login(credentials: UserLogin):
    db = get_db()

    # ----------------------------------------
    # USER DHUNDO
    # ----------------------------------------
    # Email se user dhundo database mein
    user = await db.users.find_one(
        {"email": credentials.email}
    )

    # User nahi mila?
    if not user:
        # Security reason se same error do
        # "Email ya password galat hai"
        # Attacker ko pata na chale
        # ki email exist karta hai ya nahi!
        raise HTTPException(
            status_code=401,
            detail="Email ya password galat hai!"
        )

    # ----------------------------------------
    # PASSWORD VERIFY KARO
    # ----------------------------------------
    # User ne dala → credentials.password
    # Database mein hai → user["password"]
    # verify_password() compare karega
    password_correct = verify_password(
        credentials.password,  # Plain password
        user["password"]       # Hashed password
    )

    # Password galat hai?
    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Email ya password galat hai!"
        )

    # ----------------------------------------
    # TOKEN BANAO AUR RETURN KARO
    # ----------------------------------------
    token = create_access_token({
        "sub": user["email"],
        "user_id": str(user["_id"])
    })

    return {
        "message": "Login successful! 👋",
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }


# ------------------------------------------------
# DEPENDENCY — get_current_user()
# ------------------------------------------------
# YE KYA KARTA HAI?
# Protected routes mein use hota hai
# Token verify karke current user return karta hai
#
# KAISE USE HOGA?
# @router.get("/profile")
# async def profile(
#     current_user = Depends(get_current_user)
# ):
#     return current_user
# ------------------------------------------------

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Header se token nikalo
    # "Authorization: Bearer eyJ..."
    #                          ↑ Ye token hai
    token = credentials.credentials

    # Token verify karo
    payload = verify_token(token)

    # Token invalid hai?
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token invalid ya expire ho gaya!"
        )

    # Database se user dhundo
    db = get_db()
    user = await db.users.find_one(
        {"email": payload["sub"]}
    )

    # User nahi mila?
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User nahi mila!"
        )

    # User return karo
    return user