import base64
import io
from PIL import Image
from fastapi import HTTPException, status


def process_and_encode_image(image_bytes: bytes) -> str:
    """
    Validates image bytes, resizes if excessively large, and returns a base64 Data URI.
    
    Args:
        image_bytes: Raw bytes of the image file.
        
    Returns:
        Base64 Data URI string (e.g. data:image/jpeg;base64,...)
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image_format = image.format if image.format else "JPEG"
        
        # Convert RGBA / P modes to RGB if saving as JPEG
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            mime_type = "image/jpeg"
            save_format = "JPEG"
        else:
            mime_type = f"image/{image_format.lower()}"
            save_format = image_format
            
        # Optional optimization: resize image if dimensions exceed 2048px while maintaining aspect ratio
        max_dimension = 2048
        if max(image.width, image.height) > max_dimension:
            image.thumbnail((max_dimension, max_dimension))
            
        buffer = io.BytesIO()
        image.save(buffer, format=save_format)
        encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return f"data:{mime_type};base64,{encoded_string}"
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file: {str(e)}"
        )
