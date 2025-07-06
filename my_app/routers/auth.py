from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
import os
import json
from functools import wraps

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

router = APIRouter()

# Initialize Supabase client if available
if SUPABASE_AVAILABLE:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    else:
        supabase = None
else:
    supabase = None


class MockUser:
    """Mock user for when Supabase is not available"""
    def __init__(self, user_id: str = "mock_user", email: str = "mock@example.com"):
        self.id = user_id
        self.email = email
        self.user_metadata = {}


async def validate_token(request: Request) -> Dict[str, Any]:
    """Validate JWT token and return user information"""
    
    # If Supabase is not available, return mock user
    if not SUPABASE_AVAILABLE or not supabase:
        return {
            "id": "mock_user",
            "email": "mock@example.com",
            "user_metadata": {}
        }
    
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Verify the JWT with Supabase
        # Note: This is a simplified example. In production, you should use proper JWT verification
        # For now, we'll try to get user info using the token
        user_response = supabase.auth.get_user(token)
        
        if user_response.user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "user_metadata": user_response.user.user_metadata or {}
        }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


async def get_current_user(request: Request) -> Dict[str, Any]:
    """Get current authenticated user"""
    return await validate_token(request)


@router.get("/user-info")
async def get_user_info(user: Dict[str, Any] = Depends(get_current_user)):
    """Get authenticated user information"""
    return {
        "id": user["id"],
        "email": user["email"],
        "user_metadata": user.get("user_metadata", {})
    }


@router.get("/status")
async def auth_status():
    """Check authentication system status"""
    return {
        "supabase_available": SUPABASE_AVAILABLE,
        "supabase_configured": supabase is not None,
        "mock_mode": not SUPABASE_AVAILABLE or supabase is None
    }


@router.post("/test-auth")
async def test_auth(user: Dict[str, Any] = Depends(get_current_user)):
    """Test authentication endpoint"""
    return {
        "message": "Authentication successful",
        "user": user
    }


def require_auth(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        # This decorator can be used to protect endpoints
        # The actual auth check is done by the Depends(get_current_user) in the endpoint
        return await f(*args, **kwargs)
    return decorated_function