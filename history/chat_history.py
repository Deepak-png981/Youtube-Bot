from langchain_core.messages import HumanMessage, SystemMessage

class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, content: str):
        self.messages.append(HumanMessage(content=content))
    
    def add_system_message(self, content: str):
        self.messages.append(SystemMessage(content=content))
    
    def add_message(self, message):
        self.messages.append(message)
    
    def get_history(self):
        return self.messages
    
    def clear_history(self):
        self.messages = []