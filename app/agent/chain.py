from typing import Any
from langchain_core.messages import SystemMessage, HumanMessage
from fastapi import HTTPException, status

from app.core.config import settings
from app.agent.prompts import PALMISTRY_SYSTEM_PROMPT, PALMISTRY_USER_INSTRUCTION
from app.schemas.palmistry import PalmistryAnalysisResponse


def get_vision_model() -> Any:
    """
    Instantiates and returns the configured multi-modal vision LLM.
    Supports Google Gemini and OpenAI GPT-4o vision models.
    """
    provider = settings.MODEL_PROVIDER.lower()
    
    if provider == "google":
        if not settings.GOOGLE_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GOOGLE_API_KEY is not configured in settings/environment."
            )
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_TOKENS,
        )
        
    elif provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured in settings/environment."
            )
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unsupported MODEL_PROVIDER '{provider}'. Must be 'google' or 'openai'."
        )


def analyze_palm_image(
    image_data_uri: str,
    dominant_hand: str = "Right",
    language: str = "English"
) -> PalmistryAnalysisResponse:
    """
    Executes the LangChain multi-modal palmistry analysis chain.
    
    Args:
        image_data_uri: Base64 data URI (e.g. data:image/jpeg;base64,...) of the hand image.
        dominant_hand: "Right" or "Left" hand context.
        language: Output language ("English" or "Persian").
        
    Returns:
        PalmistryAnalysisResponse Pydantic model with structured palm reading analysis.
    """
    llm = get_vision_model()
    
    # Bind structured output model to LLM
    structured_llm = llm.with_structured_output(PalmistryAnalysisResponse)
    
    # Construct multi-modal message sequence
    messages = [
        SystemMessage(content=PALMISTRY_SYSTEM_PROMPT.format(language=language)),
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": PALMISTRY_USER_INSTRUCTION.format(dominant_hand=dominant_hand, language=language)
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_data_uri}
                }
            ]
        )
    ]
    
    try:
        # Run LangChain invocation
        response = structured_llm.invoke(messages)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error executing LangChain multi-modal analysis: {str(e)}"
        )
