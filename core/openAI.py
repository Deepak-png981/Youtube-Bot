from langchain_openai import ChatOpenAI
from config import settings

class OpenAIAPI:
    def __init__(self):
        self.llm = ChatOpenAI(api_key=settings.openai_api_key)

    def get_response(self, messages):
        try:
            response = self.llm(messages)
            return response.content.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None