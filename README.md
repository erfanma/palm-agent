# Palmistry AI Agent Service with LangChain

An intelligent, multi-modal AI service built with **LangChain**, **FastAPI**, and **Pydantic** designed to visually analyze hand images and produce structured palmistry (chiromancy & chirognomy) readings.

---

## 🌟 Key Features

- **Multi-Modal Vision Analysis**: Analyzes hand shape, finger proportions, major palm lines (Life, Head, Heart, Fate), and palm mounts (Venus, Jupiter, Saturn, Apollo/Sun, Mercury, Luna/Moon, Mars).
- **Structured Pydantic Output**: Utilizes LangChain's `.with_structured_output()` mechanism to output well-typed, validated JSON responses.
- **Provider Agnostic**: Configurable support for both **Google Gemini** (`gemini-1.5-flash` / `gemini-1.5-pro`) and **OpenAI** (`gpt-4o`).
- **RESTful FastAPI Service**:
  - `POST /api/v1/analyze-palm/upload`: Form-data image file upload (`.jpg`, `.png`, `.webp`).
  - `POST /api/v1/analyze-palm/base64`: Base64 image payload or Data URI string.
  - Interactive OpenAPI Swagger docs at `/docs`.

---

## 🏗️ Architecture & Directory Structure

```
palm_agent/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── core/
│   │   ├── config.py             # Settings management (Pydantic BaseSettings)
│   │   └── utils.py              # Base64 image encoding & preprocessing
│   ├── schemas/
│   │   └── palmistry.py          # Pydantic schemas for structured LLM output & API requests
│   ├── agent/
│   │   ├── prompts.py            # Expert Palmistry system prompt
│   │   └── chain.py              # LangChain vision chain & model bindings
│   └── routers/
│       └── analyze.py            # FastAPI endpoints for image analysis
├── .env.example                  # Environment configuration template
├── requirements.txt              # Project dependencies
├── test_client.py                # Standalone test runner & synthetic image generator
└── README.md                     # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Virtual Environment

Ensure Python 3.10+ is installed:

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Choose provider: 'google' or 'openai'
MODEL_PROVIDER=google

# For Google Gemini
GOOGLE_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-1.5-flash

# For OpenAI (Alternative)
# MODEL_PROVIDER=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o
```

---

## 📡 Running the FastAPI Service

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## 🧪 Example API Requests

### 1. File Upload Request (`cURL`)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analyze-palm/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/hand_photo.jpg;type=image/jpeg' \
  -F 'dominant_hand=Right'
```

### 2. Base64 Payload Request (`cURL`)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/analyze-palm/base64' \
  -H 'Content-Type: application/json' \
  -d '{
    "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "dominant_hand": "Right"
  }'
```

---

## 📊 Output Schema Example

```json
{
  "is_hand_detected": true,
  "detection_message": null,
  "hand_element": {
    "element": "Air Hand",
    "palm_to_finger_ratio": "Square palm with long, elegant fingers",
    "summary": "Intellectual, communicative, and detail-oriented."
  },
  "major_lines": {
    "life_line": {
      "present": true,
      "clarity": "Deep & Clear",
      "length_and_depth": "Sweeping curve extending around the thumb mount",
      "interpretation": "High vitality, strong physical resilience, and adaptability."
    },
    "head_line": {
      "present": true,
      "clarity": "Slightly sloping toward Moon mount",
      "length_and_depth": "Long and distinct",
      "interpretation": "Creative problem solving combined with analytical depth."
    },
    "heart_line": {
      "present": true,
      "clarity": "Clear curve terminating under index finger",
      "length_and_depth": "Unbroken",
      "interpretation": "Warmth, idealist in relationships, open emotional expression."
    },
    "fate_line": {
      "present": true,
      "clarity": "Faint but visible",
      "length_and_depth": "Starts mid-palm running vertically",
      "interpretation": "Self-driven path with career evolution after early adult years."
    }
  },
  "mounts": {
    "venus": {
      "prominence": "Well-developed",
      "traits": "Strong capacity for empathy, enjoyment of life, and emotional warmth."
    },
    "jupiter": {
      "prominence": "Prominent",
      "traits": "Natural leadership abilities and self-confidence."
    },
    "saturn": {
      "prominence": "Moderate",
      "traits": "Balanced sense of responsibility and discipline."
    },
    "sun_apollo": {
      "prominence": "Well-developed",
      "traits": "Appreciation for aesthetics, art, and creative self-expression."
    },
    "mercury": {
      "prominence": "Flat to moderate",
      "traits": "Pragmatic approach to business and clear communication."
    },
    "moon_luna": {
      "prominence": "Prominent",
      "traits": "Rich imagination, strong intuition, and introspective nature."
    },
    "mars": {
      "prominence": "Balanced",
      "traits": "Resilience in overcoming challenges and steady courage."
    }
  },
  "personality_insights": {
    "core_strengths": [
      "Intuitive decision making",
      "Artistic and creative vision",
      "Strong empathetic connections"
    ],
    "emotional_profile": "Expressive and warm, valuing harmony and genuine connection.",
    "intellectual_style": "Combines imaginative conceptual thinking with analytical focus.",
    "growth_opportunities": [
      "Setting clear personal boundaries",
      "Balancing high ideals with practical execution"
    ]
  },
  "overall_summary": "Your hand reveals a vibrant combination of an Air Hand archetype with strong creative and intuitive markers. The clear Heart and Head lines suggest a harmonious balance between emotional openness and intellectual clarity.",
  "disclaimer": "Palmistry readings are provided for self-reflection, personal insight, and entertainment purposes only."
}
```

---

## 🛠️ Verification & Testing

To test Python module imports and structure:

```bash
python test_client.py
```

---

## 📜 License & Safety

This project is licensed under the MIT License. Palm readings generated by AI models are for entertainment and self-reflection.
