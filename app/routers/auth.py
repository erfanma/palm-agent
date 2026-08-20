from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from app.schemas.user import LoginSchema, UserInfoSchema
from app.db import database

router = APIRouter(prefix="/api", tags=["Authentication & User Management"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(credentials: LoginSchema):
    user = database.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است"
        )
    
    # Retrieve user historical readings
    user_readings = database.get_user_readings_db(credentials.username)
    
    return {
        "status": "success",
        "message": "ورود با موفقیت انجام شد",
        "user": user,
        "readings": user_readings
    }

@router.post("/user_info", status_code=status.HTTP_200_OK)
def save_user_info(user_data: UserInfoSchema):
    try:
        user_dict = user_data.model_dump() if hasattr(user_data, "model_dump") else user_data.dict()
        user_id = database.save_or_update_user(user_dict)
        return {
            "status": "success",
            "message": "User information saved successfully",
            "user_id": user_id,
            "username": user_data.username
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save user info: {str(e)}"
        )

@router.get("/users", response_model=List[Dict[str, Any]])
def list_users():
    return database.get_all_users()

@router.get("/user_info/{username}")
def get_user(username: str):
    user = database.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{username}' not found"
        )
    return user
