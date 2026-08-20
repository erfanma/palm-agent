from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class LoginSchema(BaseModel):
    username: str = Field(..., min_length=1, example="user123")
    password: str = Field(..., min_length=1, example="pass123")

class UserInfoSchema(BaseModel):
    username: str = Field(..., min_length=2, example="user123")
    password: str = Field(..., min_length=3, example="pass123")
    first_name: str = Field(..., example="Ali")
    last_name: str = Field(..., example="Rezai")
    date_of_birth: str = Field(..., example="1995-04-15")
    gender: str = Field(..., example="Male")
    palmistry_info: Dict[str, Any] = Field(
        default_factory=dict, 
        example={"dominant_hand": "Right", "hand_size": "Medium", "active_lines": ["line_life", "line_head"]}
    )
