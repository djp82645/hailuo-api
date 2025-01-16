from typing import Any, Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    code: Optional[int] = 0
    msg: Optional[str] = "success"
    data: Optional[Any] = None


class CustomModeGenerateParam(BaseModel):
    """Generate with Custom Mode"""

    prompt: str = Field(..., description="lyrics")
    mv: str = Field(
        default="chirp-v4",
        description="model version, default: chirp-v4",
        examples=["chirp-v4"],
    )
    title: str = Field(..., description="song title")
    tags: str = Field(..., description="style of music")
    continue_at: Optional[float] = Field(
        default=None,
        description="continue a new clip from a previous song, format number",
        examples=[120],
    )
    continue_clip_id: Optional[str] = None


class DescriptionModeGenerateParam(BaseModel):
    """Generate with Video Description"""

    md: str = Field(
        default="minimax-i2v",
        description="model version, default: minimax-i2v",
        examples=["minimax-i2v"],
    )

    prompt: str = Field(
        default="",
        description="Placeholder, keep it as an empty string, do not modify it",
    )
    callback:bool = False

class TaskParam(BaseModel):
    """get video task detail"""

    task_id: str

class GenerateLyricsParam(BaseModel):
    prompt: str = Field(..., description="lyrics")
