from pydantic import BaseModel, Field
from typing import Dict, Any

class WizardReadingSchema(BaseModel):
    username: str = Field(..., min_length=1, example="user123")
    selections: Dict[str, Any] = Field(
        ..., 
        example={"handShape": "earth", "activeHand": "right_active", "heartLine": "long_curved"}
    )
