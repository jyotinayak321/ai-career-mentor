# ================================================
# mongodb.py
# ================================================
# YE FILE KYA KARTI HAI?
# MongoDB database se connection banati hai
#
# ANALOGY:
# MongoDB = Ek bada library building 📚
# mongodb.py = Library ka entrance gate
# connect_db() = Gate kholna
# close_db() = Gate band karna
# get_db() = Andar jaane ka rasta dena
# ================================================


# ------------------------------------------------
# IMPORTS — Zaroori tools mangwao
# ------------------------------------------------

# motor = MongoDB ka async driver
# AsyncIOMotorClient = Connection banane ki class
# "Async" matlab = Ek kaam hote hue
#                  doosre kaam bhi chalte rahenge
#                  Server ruka nahi rahega!
from motor.motor_asyncio import AsyncIOMotorClient

# config.py se settings import karo
# settings mein hai:
# → MONGODB_URL = "mongodb://localhost:27017"
# → DB_NAME = "career_mentor_db"
from config import settings


# ------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------
# "Global" matlab = Poori file mein use hoga
#
# Abhi dono NONE hain — matlab khali hain
# connect_db() chalega tab bharenge
#
# client = MongoDB ka connection object
#          Jaise phone ka dial tone
#          Connection bana hai ya nahi
#
# db = Database object
#      Jaise specific library section
#      "Career Mentor" section select karna
# ------------------------------------------------

client = None   # Abhi koi connection nahi
db = None       # Abhi koi database select nahi


# ------------------------------------------------
# FUNCTION 1 — connect_db()
# ------------------------------------------------
# YE FUNCTION KYA KARTA HAI?
# Server start hone pe MongoDB se connect karta hai
#
# "async" kyu likha?
# Kyunki ye network operation hai
# Time lagta hai connect hone mein
# Is time mein server doosre kaam kar sake
# Isliye async likha!
#
# Kab call hota hai ye?
# main.py mein startup_event() mein:
# @app.on_event("startup")
# async def startup_event():
#     await connect_db()  ← Yahan call hota hai
# ------------------------------------------------

async def connect_db():
    
    # "global" keyword kyu?
    # Agar global nahi likhte toh
    # ye function apne andar naye
    # client aur db banata
    # Bahar wale change nahi hote!
    #
    # global likhne se bahar wale
    # client aur db change honge ✅
    global client, db
    
    # MongoDB se connection banao
    # AsyncIOMotorClient = Connection class
    # settings.MONGODB_URL = "mongodb://localhost:27017"
    #
    # ANALOGY:
    # Jaise phone mein number dial karna
    # 27017 = MongoDB ka default port number
    # Port = Ghar ka door number 🚪
    client = AsyncIOMotorClient(
        settings.MONGODB_URL
        # = "mongodb://localhost:27017"
    )
    
    # Database select karo
    # settings.DB_NAME = "career_mentor_db"
    #
    # ANALOGY:
    # Library mein specific section select karna
    # "Career Mentor" naam ka dabba kholo
    # Isme saara hamaara data hoga:
    # → users collection
    # → resumes collection  
    # → jobs collection
    db = client[settings.DB_NAME]
    # = client["career_mentor_db"]
    
    # Success messages print karo
    # Terminal mein dikhega server start hone pe
    print("✅ MongoDB Connected!")
    print(f"✅ Database: {settings.DB_NAME}")
    # Output hoga:
    # ✅ MongoDB Connected!
    # ✅ Database: career_mentor_db


# ------------------------------------------------
# FUNCTION 2 — close_db()
# ------------------------------------------------
# YE FUNCTION KYA KARTA HAI?
# Server band hone pe connection close karta hai
#
# Kyu zaroori hai close karna?
# Jaise:
# → Ghar jaate waqt light band karna
# → Phone call khatam hone pe hang up karna
# → Dukaan band karne pe tala lagana
#
# Agar close nahi kiya toh:
# → Memory leak ho sakti hai
# → MongoDB pe unnecessary load
# → Resources waste honge
#
# Kab call hota hai?
# main.py mein shutdown_event() mein:
# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()  ← Yahan call hota hai
# ------------------------------------------------

async def close_db():
    
    # "global client" kyu?
    # Upar banaye gaye client ko
    # is function mein use karna hai
    global client
    
    # Pehle check karo —
    # client exist karta hai ya nahi?
    # Agar server connect hi nahi hua tha
    # toh close karne ki zaroorat nahi
    if client:
        # Connection band karo
        client.close()
        
        # Confirmation message
        print("MongoDB connection closed! 👋")


# ------------------------------------------------
# FUNCTION 3 — get_db()
# ------------------------------------------------
# YE FUNCTION KYA KARTA HAI?
# Database object return karta hai
# Taaki doosri files use kar sakein
#
# ANALOGY:
# Library mein receptionist
# Jo tumhe sahi section tak le jaaye
#
# KAISE USE HOGA POORE PROJECT MEIN?
#
# Resume save karna:
# db = get_db()
# await db.resumes.insert_one({...})
#
# User dhundna:
# db = get_db()
# user = await db.users.find_one(
#     {"email": "jyoti@gmail.com"}
# )
#
# Jobs fetch karna:
# db = get_db()
# jobs = await db.jobs.find({}).to_list(10)
# ------------------------------------------------

def get_db():
    # db variable return karo
    # Jo connect_db() mein set hua tha
    #
    # Note: Ye async nahi hai!
    # Kyunki ye sirf variable return karta hai
    # Koi network operation nahi hai
    return db