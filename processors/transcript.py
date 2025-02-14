from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import settings
from prompts.generate_notes import SYSTEM_PROMPT
class NoteGenerator:
    def __init__(self, model_name="gpt-4o"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.3 , api_key=settings.openai_api_key)

    def generate_notes(self, transcript: str) -> str:
        system_prompt = SYSTEM_PROMPT
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Transcript:\n{transcript}")
        ]
        
        return self.llm(messages).content