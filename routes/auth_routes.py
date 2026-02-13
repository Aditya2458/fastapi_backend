from fastapi import APIRouter, HTTPException, status
from schemas import UserSignup, UserLogin
from auth import hash_password, verify_password, create_access_token
from crud import create_user, get_user_by_email

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    hashed = hash_password(user.password)
    create_user(user, hashed)
    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user["id"])})

    return {
        "access_token": token,
        "token_type": "bearer"
    }