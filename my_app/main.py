from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from my_app.routers import translate, auth

app = FastAPI(
    title="Translation Service",
    description="Asynchronous translation service using FastAPI and Supabase",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(translate.router, prefix="/translate", tags=["Translation"])

# Mount static files from frontend directory
frontend_path = Path("frontend")
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    print("📁 Frontend static files mounted at /static")

@app.get("/")
async def root():
    """Serve the main dashboard page"""
    index_path = Path("frontend/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Translation Service API", "version": "0.1.0"}

@app.get("/dashboard")
async def dashboard():
    """Alternative route to the dashboard"""
    index_path = Path("frontend/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "Dashboard not found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}