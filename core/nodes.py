from .state import ChatState
from processors.youtube import YouTubeProcessor
from processors.generator import Generator
from .utils import extract_video_id
import re
from history.chat_history import ChatHistory
def route_input(state: ChatState) -> str:
    if "youtube.com" in state.user_input:
        return "youtube_flow"
    return "normal_chat"

class GraphNodes:
    def __init__(self):
        self.youtube_processor = YouTubeProcessor()
        self.generator = Generator()
        self.chat_history = ChatHistory()
    
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
        state.notes = self.generator.generate_response(state.user_input , state.transcript, self.chat_history.get_history())
        self._update_history(state)
        return state
    