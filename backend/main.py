from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.mongodb import connect_db, close_db
from api.auth import router as auth_router
from api.resume import router as resume_router
from api.jobs import router as jobs_router
from api.roadmap import router as roadmap_router
from api.interview import router as interview_router
from api.agent import router as agent_router

app = FastAPI(
    title="AI Career Mentor API",
    description="Autonomous AI system for career guidance",
    version="1.0.0",
    # Docs enable karo
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://ai-career-mentor-sage.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    resume_router,
    prefix="/api/resume",
    tags=["Resume"]
)

app.include_router(
    jobs_router,
    prefix="/api/jobs",
    tags=["Jobs"]
)

app.include_router(
    roadmap_router,
    prefix="/api/roadmap",
    tags=["Roadmap"]
)

app.include_router(
    interview_router,
    prefix="/api/interview",
    tags=["Interview"]
)

app.include_router(
    agent_router,
    prefix="/api/agent",
    tags=["AI Agent"]
)

@app.get("/")
async def root():
    return {
        "message": "AI Career Mentor API chal raha hai!",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    print("Server Start Ho Raha Hai...")
    await connect_db()
    print("Server Ready!")

@app.on_event("shutdown")
async def shutdown_event():
    print("Server Band Ho Raha Hai...")
    await close_db()
    