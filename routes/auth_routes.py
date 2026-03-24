from fastapi import APIRouter, HTTPException, status
from schemas import UserSignup, UserLogin
from auth import hash_password, verify_password, create_access_token
from crud import create_user, get_user_by_email
from schemas import ForgotPasswordRequest
from auth import create_reset_token
from crud import update_user_password
from schemas import ResetPasswordRequest
from jose import JWTError, jwt
from auth import hash_password, SECRET_KEY, ALGORITHM
from metrics import login_success_total, login_failures_total

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
        login_failures_total.inc()   # ❌ failed login
        raise HTTPException(status_code=401, detail="Invalid credentials")

    login_success_total.inc()       # ✅ successful login

    token = create_access_token({
        "sub": str(db_user["id"]),
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# here this is for reset password token generation


@router.post("/forgot_password")
def forget_password(request:ForgotPasswordRequest):
    user= get_user_by_email(request.email)

    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    
    reset_token= create_reset_token(user["id"])

    return{
        "message":"password reset token generated",
        "reset_token": reset_token
    }


# here am creating routes for reset password

@router.post("/reset_password")
def reset_password(request: ResetPasswordRequest):

    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    if payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    user_id= payload.get("sub")

    hashed_password = hash_password(request.new_password)
    update_user_password(user_id, hashed_password)
    return {"message": "Password reset successfully"}

