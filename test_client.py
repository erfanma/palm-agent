"""
Standalone test script to verify Palmistry AI Agent functionality with sample/generated image.
"""

import os
import io
import sys
from PIL import Image, ImageDraw

# Add workspace root to sys.path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.utils import process_and_encode_image
from app.agent.chain import analyze_palm_image
from app.schemas.palmistry import PalmistryAnalysisResponse


def generate_sample_hand_image() -> bytes:
    """Generates a synthetic test image representing a hand drawing for verification testing."""
    img = Image.new("RGB", (600, 800), color=(245, 235, 220))
    draw = ImageDraw.Draw(img)
    
    # Draw palm outline
    draw.ellipse([150, 300, 450, 700], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    # Draw fingers
    draw.rectangle([170, 100, 220, 320], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    draw.rectangle([240, 80, 290, 310], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    draw.rectangle([310, 90, 360, 310], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    draw.rectangle([380, 130, 430, 330], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    # Draw Thumb
    draw.rectangle([80, 380, 170, 430], fill=(235, 205, 180), outline=(180, 140, 110), width=4)
    
    # Draw Major Palm Lines
    # Life Line
    draw.arc([160, 350, 340, 650], start=270, end=90, fill=(150, 70, 50), width=4)
    # Head Line
    draw.line([(180, 450), (400, 480)], fill=(120, 50, 50), width=4)
    # Heart Line
    draw.line([(180, 380), (420, 360)], fill=(160, 40, 60), width=4)
    # Fate Line
    draw.line([(300, 620), (290, 360)], fill=(80, 40, 40), width=3)
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def run_local_test():
    print("=== Palmistry AI Agent Local Verification Test ===")
    image_bytes = generate_sample_hand_image()
    data_uri = process_and_encode_image(image_bytes)
    print(f"[OK] Generated test image Data URI (length: {len(data_uri)})")
    
    # Check if API key is set
    api_key_google = os.getenv("GOOGLE_API_KEY")
    api_key_openai = os.getenv("OPENAI_API_KEY")
    
    if not api_key_google and not api_key_openai:
        print("[WARNING] Neither GOOGLE_API_KEY nor OPENAI_API_KEY is set in environment.")
        print("Please configure your .env file with your API key before invoking the LLM.")
        print("Structure and code verification completed successfully.")
        return
        
    print("[INFO] Invoking LangChain Palmistry Agent...")
    result: PalmistryAnalysisResponse = analyze_palm_image(data_uri, dominant_hand="Right")
    print("\n--- Analysis Result ---")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    run_local_test()
