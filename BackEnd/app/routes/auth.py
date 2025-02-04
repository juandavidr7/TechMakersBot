from fastapi import APIRouter, Depends
from ..auth_model import LoginRequest, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    return AuthService.authenticate_user(request)
