from langchain_core.messages import HumanMessage, SystemMessage
from prompts.generate_notes import SYSTEM_PROMPT
from core.openAI import OpenAIAPI
from prompts.generate_response import generate_response_prompt
class Generator:
    def __init__(self):
        self.llm = OpenAIAPI()

    def generate_notes(self, transcript: str) -> str:
        system_prompt = SYSTEM_PROMPT
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Transcript:\n{transcript}")
        ]
        
        response = self.llm.get_response(messages)
        return response
    
    def generate_response(self, user_input: str, transcript: str, chat_history: list) -> str:
        system_prompt, human_prompt = generate_response_prompt(user_input, transcript, chat_history)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.get_response(messages)
        return response

