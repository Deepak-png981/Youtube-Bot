from core.graph import ChatGraph
from core.utils import setup_logging
import logging
# from dotenv import load_dotenv
# import os

# load_dotenv()

class ChatBotCLI:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.graph = ChatGraph()
    
    def run(self):
        print("Welcome to SmartChat! (Type 'q' to quit)")
        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() == 'q':
                    break
                
                result = self.graph.execute(user_input)
                self._display_result(result)
            
            except Exception as e:
                self.logger.error(f"Error processing request: {str(e)}")
                print("Sorry, I encountered an error. Please try again.")
    
    def _display_result(self, state):
        print("\nAssistant:")
        print("FINAL STATE:")
        print(state)
        if state.notes:
            print(state.notes)
        else:
            print("No response generated")

if __name__ == "__main__":
    ChatBotCLI().run()