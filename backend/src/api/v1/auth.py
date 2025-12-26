from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.core.security import create_access_token, get_current_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    email: str
    name: str

@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest):
    # Lógica Mock para el MVP (Usuario único)
    # En producción esto validaría contra la base de datos
    if form_data.email == "user@financial.com" and form_data.password == "password":
        access_token = create_access_token(data={"sub": form_data.email})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Incorrect email or password")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado.
    Requiere un token JWT válido en el header Authorization.
    """
    # En producción, aquí consultarías la base de datos para obtener más información del usuario
    return {
        "email": current_user["email"],
        "name": "Usuario Demo"
    }