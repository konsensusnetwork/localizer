from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
async def root():
    return {"message": "Translation Service API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}