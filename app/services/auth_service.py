from fastapi import HTTPException
from app.auth_model import LoginRequest, LoginResponse

users_db = {
    "admin": {"password": "123456", "role": "admin"},
    "usuario": {"password": "prueba123", "role": "user"},
}


class AuthService:
    @staticmethod
    def authenticate_user(request: LoginRequest) -> LoginResponse:
        user = users_db.get(request.username)
        if not user or user["password"] != request.password:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        return LoginResponse(role=user["role"])
