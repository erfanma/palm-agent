from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from app.core.utils import process_and_encode_image
from app.schemas.palmistry import PalmistryAnalysisResponse, AnalyzeBase64Request
from app.agent.chain import analyze_palm_image

router = APIRouter(prefix="/api/v1/analyze-palm", tags=["Palmistry Analysis"])


@router.post(
    "/upload",
    response_model=PalmistryAnalysisResponse,
    summary="Analyze Palm Image File Upload",
    description="Upload a hand image file (JPEG, PNG, WEBP) to perform palmistry AI analysis."
)
async def analyze_palm_file(
    file: UploadFile = File(..., description="Hand image file to analyze"),
    dominant_hand: str = Form("Right", description="Dominant hand: 'Right' or 'Left'"),
    language: str = Form("English", description="Target output language: 'Persian' or 'English'")
) -> PalmistryAnalysisResponse:
    """Endpoint handling direct image file uploads."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided is not an image."
        )
        
    image_bytes = await file.read()
    image_data_uri = process_and_encode_image(image_bytes)
    
    return analyze_palm_image(
        image_data_uri=image_data_uri,
        dominant_hand=dominant_hand,
        language=language
    )


@router.post(
    "/base64",
    response_model=PalmistryAnalysisResponse,
    summary="Analyze Palm Base64 or Data URI",
    description="Send a base64 encoded string or Data URI of a hand image to perform palmistry AI analysis."
)
async def analyze_palm_base64(
    request: AnalyzeBase64Request
) -> PalmistryAnalysisResponse:
    """Endpoint handling Base64 JSON payloads."""
    image_str = request.image_base64.strip()
    
    # Format data URI if plain base64 string was sent
    if not image_str.startswith("data:image/"):
        image_data_uri = f"data:image/jpeg;base64,{image_str}"
    else:
        image_data_uri = image_str
        
    return analyze_palm_image(
        image_data_uri=image_data_uri,
        dominant_hand=request.dominant_hand,
        language=request.language or "English"
    )
