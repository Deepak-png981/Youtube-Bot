from .state import ChatState
from processors.youtube import YouTubeProcessor
from processors.generator import Generator
from .utils import extract_video_id
import re
from history.chat_history import ChatHistory
from core.openAI import OpenAIAPI
from processors.tools import export_notes

def route_input(state: ChatState) -> str:
    if "youtube.com" in state.user_input:
        return "youtube_flow"
    return "normal_chat"

class Message:
    def __init__(self, role: str, content: str, tool_calls: list = None):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls or []

class GraphNodes:
    def __init__(self):
        self.youtube_processor = YouTubeProcessor()
        self.generator = Generator()
        self.chat_history = ChatHistory()
        self.openai = OpenAIAPI()
    
    def detect_youtube_url(self, state: ChatState) -> ChatState:
        youtube_url_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)'
        match = re.search(youtube_url_pattern, state.user_input)
        if match:
            state.youtube_url = match.group(0)
        else:
            state.youtube_url = None
        return state
    
    def extract_transcript(self, state: ChatState) -> ChatState:
        video_id = extract_video_id(state.youtube_url)
        state.video_id = video_id
        state.transcript = self.youtube_processor.get_transcript(video_id)
        return state
    
    def _update_history(self, state: ChatState) -> None:
        self.chat_history.add_user_message(state.user_input)
        self.chat_history.add_system_message(state.notes)
    
    def generate_notes(self, state: ChatState) -> ChatState:
        state.notes = self.generator.generate_notes(state.transcript)
        self._update_history(state)
        return state
    
    def normal_chat_response(self, state: ChatState) -> ChatState:
        print("normal_chat_response")
        state.notes = self.generator.generate_response(state.user_input , state.transcript, self.chat_history.get_history())
        self._update_history(state)
        return state
    def should_export(self, state: ChatState):
        print("Entering should_export with state:", state)
        
        llm_with_tools = self.openai.bind_tools([export_notes])    
        prompt = state.user_input + "\n\n" + state.notes
        messages = [{"role": "user", "content": prompt}]
        
        print("Sending messages to LLM:", messages)
        decision = llm_with_tools.invoke(messages)
        print("Received decision from LLM:", decision)
        return {"messages" : decision}



        # tool_calls = None
        # if isinstance(decision, dict):
        #     tool_calls = decision.get("tool_calls") or decision.get("additional_kwargs", {}).get("tool_calls", [])
        # elif hasattr(decision, "additional_kwargs"):
        #     tool_calls = decision.additional_kwargs.get("tool_calls", [])

        # print("Extracted tool_calls:", tool_calls)

        # if tool_calls:
        #     print("Tool calls found:", tool_calls)
        #     state.tool = tool_calls[0]
        #     state.action = "tools"
        # else:
        #     print("No tool calls found, setting action to respond")
        #     state.action = "respond"
        
        # print("Exiting should_export with state:", state)
        # return state

   
    
    