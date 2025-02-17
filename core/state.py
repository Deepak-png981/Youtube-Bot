from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from langchain_core.messages import BaseMessage

class ChatState(BaseModel):
    user_input: str
    youtube_url: Optional[str] = None
    video_id: Optional[str] = None
    transcript: Optional[str] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    action: Optional[str] = None
    tool: Optional[Dict] = None
    messages: List[BaseMessage] = Field(default_factory=list)
