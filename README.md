🚀AI Career Mentor is a full-stack AI-powered career guidance platform that helps students and 🧠professionals accelerate their career growth. It analyzes resumes, detects skill gaps, recommends jobs👨‍🎓, generates personalized learning roadmaps, and conducts AI mock interviews.

Built with FastAPI, React, MongoDB, Groq LLaMA-3.3, LangChain, FAISS, and RAG System.


✨ Features
FeatureDescription📄 Resume AnalyzerUpload PDF/DOCX resume and get instant AI-powered score out of 100🎯 Skill Gap DetectionIdentify missing skills for your target role💼 Job RecommendationsGet personalized job matches with apply links (LinkedIn, Naukri, Indeed)🗺️ Career RoadmapAI-generated weekly learning plan for your target role🎤 Mock InterviewPractice with AI interviewer — type or speak your answers🤖 AI Career AgentChat with Groq-powered LLaMA agent for career guidance🔍 RAG SystemKnowledge base with FAISS vector search for accurate answers🛡️ Defence AI JobsDedicated section for DRDO, IAF, iDEX opportunities

🛠️ Tech Stack
Backend

FastAPI — High-performance Python web framework
MongoDB Atlas — Cloud NoSQL database
Groq + LLaMA-3.3-70B — Free AI inference (ultra-fast!)
LangChain — LLM orchestration framework
FAISS — Facebook AI Similarity Search (vector database)
spaCy — NLP for resume parsing
pdfplumber — PDF text extraction
JWT — Secure authentication

Frontend

React 18 — Modern UI library
Vite — Lightning-fast build tool
React Router DOM — Client-side routing
Axios — HTTP client with interceptors

Deployment

Render — Backend hosting (Free tier)
Vercel — Frontend hosting (Free tier)
MongoDB Atlas — Database (Free tier)


🏗️ Project Structure

```bash

ai-career-mentor/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Environment variables
│   ├── requirements.txt
│   ├── api/
│   │   ├── auth.py              # Login, register endpoints
│   │   ├── resume.py            # Resume upload endpoint
│   │   ├── jobs.py              # Job recommendation endpoint
│   │   ├── roadmap.py           # Roadmap endpoint
│   │   ├── interview.py         # Interview endpoint
│   │   └── agent.py             # AI agent endpoint
│   ├── agents/
│   │   └── career_agent.py      # Groq multi-tool agent
│   ├── resume_parser/
│   │   ├── parser.py            # Resume parser
│   │   └── scorer.py            # Resume scoring logic
│   ├── skill_gap/
│   │   └── detector.py          # Skill gap detection
│   ├── job_recommender/
│   │   ├── recommender.py       # Job matching logic
│   │   ├── real_jobs.py         # RapidAPI JSearch integration
│   │   └── mock_jobs.json       # Sample job data
│   ├── roadmap/
│   │   └── generator.py         # LLM-based roadmap generator
│   ├── interview/
│   │   └── simulator.py         # Mock interview module
│   ├── rag_system/
│   │   ├── vectorstore.py       # FAISS vector store
│   │   ├── ingestion.py         # Knowledge ingestion
│   │   └── retriever.py         # RAG retrieval
│   ├── database/
│   │   └── mongodb.py           # MongoDB connection
│   └── utils/
│       ├── jwt_handler.py       # JWT token logic
│       └── file_handler.py      # PDF/DOCX extraction
│
└── frontend/
    ├── src/
    │   ├── App.jsx              # Routes
    │   ├── api/
    │   │   └── axios.js         # API calls with interceptors
    │   ├── components/
    │   │   └── Navbar.jsx       # Navigation component
    │   └── pages/
    │       ├── Login.jsx
    │       ├── Register.jsx
    │       ├── Dashboard.jsx    # Career overview + skill gap
    │       ├── ResumeUpload.jsx # Resume analyzer
    │       ├── JobSearch.jsx    # Job recommendations
    │       ├── Roadmap.jsx      # Career roadmap generator
    │       └── Interview.jsx    # Mock interview (type/speak)
    ├── package.json
    └── vite.config.js
```

🚀 Getting Started
Prerequisites
bashPython 3.11+
Node.js 18+
MongoDB Atlas account (free)
Groq API key (free)
Backend Setup
bash# Clone the repo
git clone https://github.com/jyotinayak321/ai-career-mentor.git
cd ai-career-mentor/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your keys to .env

# Initialize knowledge base
python rag_system/ingestion.py

# Start server
uvicorn main:app --reload
Frontend Setup
bashcd ../frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env

# Start development server
npm run dev
Environment Variables
Create backend/.env:
envMONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/career_mentor_db
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
RAPIDAPI_KEY=your-rapidapi-key
ANTHROPIC_API_KEY=your-anthropic-key (optional)

📡 API Endpoints
MethodEndpointDescriptionPOST/api/auth/registerRegister new userPOST/api/auth/loginLogin userPOST/api/resume/uploadUpload & analyze resumeGET/api/jobs/recommendGet job recommendationsPOST/api/roadmap/generateGenerate career roadmapPOST/api/interview/startStart mock interviewPOST/api/interview/answerSubmit interview answerPOST/api/agent/chatChat with AI agentGET/api/agent/tipsGet personalized tips
Full API documentation: https://ai-career-mentor-iu6h.onrender.com/docs

🎯 Key Highlights

100% Free Stack — Groq (free), MongoDB Atlas (free), Render (free), Vercel (free)
RAG System — 8 career knowledge documents indexed in FAISS for accurate AI responses
Real Job Links — Direct apply buttons for LinkedIn, Naukri, Indeed, Company sites
Defence AI Focus — Special job categories for DRDO, IAF, iDEX, ISRO opportunities
Speech Recognition — Mock interview supports voice answers via Web Speech API
JWT Authentication — Secure token-based auth with auto-refresh


📸 Screenshots
Login Page
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/253ba03b-8029-4b8f-9a4e-13e8371fc635" />

Beautiful gradient login page with form validation

Dashboard

Career overview with skill gap analysis, match percentage, and quick actions
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/39a8d29d-82b9-47c5-8f07-73db07d3100e" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/844978a0-3d9e-47b7-ae73-514102013e7f" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/231a11fa-31e6-410e-8453-ea5eeb9068f1" />



Resume Analyzer

Drag & drop resume upload with instant AI score, skills detection, and feedback

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f21acd5c-7543-47ca-803f-9bad3bdd8999" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/23fd0228-478b-4671-8261-27a4dfad974f" />


Job Recommendations

20+ jobs with match score, apply deadline, LinkedIn/Naukri/Company apply buttons
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d78a0d5f-9ccf-452a-923c-6625bcf24099" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/55e58d53-1624-4018-a537-7ea3304af797" />



Career Roadmap

AI-generated 12-week personalized learning plan with daily tasks

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/08cb789a-f2c7-46d8-a98b-3c8435b8f8ba" />


Mock Interview

AI interviewer with real-time feedback, score, strengths & improvements
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8030dc7b-a373-4b04-b1ce-e4d38f300945" />


🤝 Contributing
Contributions are welcome!
bash# Fork the repo
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add some AmazingFeature'

# Push to the branch
git push origin feature/AmazingFeature

# Open a Pull Request


👩‍💻 Author
Jyoti Nayak

🎓 B.Tech CSE, CBS Group of Institutes (MDU)
💼 Aspiring Software Engineer | AI/ML Enthusiast
🛡️ Defence AI Interest (IAF, DRDO, iDEX)
📧 GitHub: @jyotinayak321


🙏 Acknowledgments

Groq — Ultra-fast free LLM inference
LangChain — LLM application framework
FastAPI — Modern Python web framework
FAISS — Efficient similarity search
Render — Free backend hosting
Vercel — Free frontend hosting
