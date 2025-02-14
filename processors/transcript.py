from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class NoteGenerator:
    def __init__(self, model_name="gpt-4o"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.3)

    def generate_notes(self, transcript: str) -> str:
        system_prompt = """You are a expert note maker. Create structured notes with:
- Key points
- Important concepts
- Summary
- Action items
Use Markdown formatting with proper headings and bullet points."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Transcript:\n{transcript}")
        ]
        
        return self.llm(messages).content