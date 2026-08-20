from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from app.schemas.readings import WizardReadingSchema
from app.db import database

router = APIRouter(prefix="/api", tags=["Wizard Readings"])

@router.post("/wizard_readings", status_code=status.HTTP_201_CREATED)
def save_wizard_reading(reading_data: WizardReadingSchema):
    try:
        reading_id = database.save_wizard_reading_db(
            username=reading_data.username, 
            selections=reading_data.selections
        )
        return {
            "status": "success",
            "message": "Palmistry wizard reading saved successfully",
            "reading_id": reading_id,
            "username": reading_data.username
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save wizard reading: {str(e)}"
        )

@router.get("/wizard_readings/{username}", response_model=List[Dict[str, Any]])
def get_wizard_readings(username: str):
    return database.get_user_readings_db(username)
