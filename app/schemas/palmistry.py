from typing import List, Optional
from pydantic import BaseModel, Field


class AnalyzeBase64Request(BaseModel):
    """Payload for Base64 image analysis request."""
    image_base64: str = Field(
        ...,
        description="Base64 encoded string or Data URI of the hand image."
    )
    dominant_hand: Optional[str] = Field(
        default="Right",
        description="Indicates whether this is the dominant or passive hand (e.g., 'Right' or 'Left')."
    )
    language: Optional[str] = Field(
        default="English",
        description="Target output language for analysis: 'Persian' (Farsi) or 'English'."
    )


class LineDetail(BaseModel):
    """Details for a specific major palm line."""
    present: bool = Field(..., description="Whether the line is clearly visible in the image.")
    clarity: str = Field(..., description="Clarity and continuity (e.g. Deep & Clear, Faint, Chained, Broken).")
    length_and_depth: str = Field(..., description="Length, depth, and curvature characteristics.")
    interpretation: str = Field(..., description="Palmistry interpretation of this line's characteristics.")


class MajorLinesAnalysis(BaseModel):
    """Analysis of the four major palm lines."""
    life_line: LineDetail = Field(..., description="Analysis of the Life Line (Vitality, physical energy, major life changes).")
    head_line: LineDetail = Field(..., description="Analysis of the Head Line (Intellect, focus, thought process).")
    heart_line: LineDetail = Field(..., description="Analysis of the Heart Line (Emotions, relationships, affection).")
    fate_line: LineDetail = Field(..., description="Analysis of the Fate/Destiny Line (Career path, external influences).")


class MountDetail(BaseModel):
    """Details for a palm mount (padded area on the palm)."""
    prominence: str = Field(..., description="Prominence level (e.g. Well-developed, Flat, Highly prominent).")
    traits: str = Field(..., description="Associated personality and energetic traits.")


class MountsAnalysis(BaseModel):
    """Analysis of key palm mounts."""
    venus: MountDetail = Field(..., description="Mount of Venus (Base of thumb - passion, love, vitality).")
    jupiter: MountDetail = Field(..., description="Mount of Jupiter (Base of index finger - ambition, leadership).")
    saturn: MountDetail = Field(..., description="Mount of Saturn (Base of middle finger - wisdom, discipline).")
    sun_apollo: MountDetail = Field(..., description="Mount of Apollo/Sun (Base of ring finger - creativity, talent, success).")
    mercury: MountDetail = Field(..., description="Mount of Mercury (Base of pinky finger - communication, commerce, quick wit).")
    moon_luna: MountDetail = Field(..., description="Mount of Moon/Luna (Base of palm opposite thumb - intuition, imagination).")
    mars: MountDetail = Field(..., description="Mount of Mars (Plain of Mars & Upper/Lower Mars - courage, resilience).")


class ElementClassification(BaseModel):
    """Classification of hand archetype by the 4 elements."""
    element: str = Field(..., description="Archetype: Earth Hand, Air Hand, Fire Hand, or Water Hand.")
    palm_to_finger_ratio: str = Field(..., description="Observation of palm shape (square/oblong) vs finger length (short/long).")
    summary: str = Field(..., description="Core personality attributes tied to this hand element.")


class PersonalityInsights(BaseModel):
    """Synthesized personality and behavioral insights."""
    core_strengths: List[str] = Field(..., description="Top personality strengths identified from hand features.")
    emotional_profile: str = Field(..., description="Emotional tendencies and interpersonal relational style.")
    intellectual_style: str = Field(..., description="Decision-making, problem-solving, and mental clarity style.")
    growth_opportunities: List[str] = Field(..., description="Key areas for personal growth and self-awareness.")


class PalmistryAnalysisResponse(BaseModel):
    """Complete Palmistry Analysis Response Schema."""
    is_hand_detected: bool = Field(
        ...,
        description="True if a human palm/hand is clearly visible in the image, False otherwise."
    )
    detection_message: Optional[str] = Field(
        default=None,
        description="Explanatory message if no hand is detected or if image quality is poor."
    )
    hand_element: Optional[ElementClassification] = Field(
        default=None,
        description="Elemental classification of hand shape and finger proportions."
    )
    major_lines: Optional[MajorLinesAnalysis] = Field(
        default=None,
        description="Detailed reading of Life, Head, Heart, and Fate lines."
    )
    mounts: Optional[MountsAnalysis] = Field(
        default=None,
        description="Detailed reading of the major palm mounts."
    )
    personality_insights: Optional[PersonalityInsights] = Field(
        default=None,
        description="Synthesized personality, emotional, and cognitive profile."
    )
    overall_summary: Optional[str] = Field(
        default=None,
        description="Comprehensive summary reading unifying all observed features into an inspiring overview."
    )
    disclaimer: str = Field(
        default="Palmistry readings are provided for self-reflection, personal insight, and entertainment purposes only.",
        description="Standard safety disclaimer."
    )
