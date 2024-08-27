from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user, milestones, tasks, progress , projects

app = FastAPI(
    title="Project Management API",
    description="API designed for managing projects, milestones, tasks, and tracking progress.",
    version="1.0.0",  
)

# Configure CORS (Cross-Origin Resource Sharing) settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(milestones.router)
app.include_router(progress.router)
