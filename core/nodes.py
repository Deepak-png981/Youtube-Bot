from .state import ChatState
from processors.youtube import YouTubeProcessor
from processors.transcript import NoteGenerator
from .utils import extract_video_id
import re

def route_input(state: ChatState) -> str:
    if "youtube.com" in state.user_input:
        print("YOUTUBE FLOW")
        return "youtube_flow"
    return "normal_chat"

class GraphNodes:
    def __init__(self):
        self.youtube_processor = YouTubeProcessor()
        self.note_generator = NoteGenerator()
    
    def detect_youtube_url(self, state: ChatState) -> ChatState:
        youtube_url_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)'
        match = re.search(youtube_url_pattern, state.user_input)
        if match:
            state.youtube_url = match.group(0)
        else:
            state.youtube_url = None
        print("YOUTUBE URL:")
        print(state.youtube_url)
        return state
    
    def extract_transcript(self, state: ChatState) -> ChatState:
        video_id = extract_video_id(state.youtube_url)
        state.video_id = video_id
        print("Video ID: ", video_id)
        state.transcript = self.youtube_processor.get_transcript(video_id)
        print("Transcript: ", state.transcript)
        return state
    
    def generate_notes(self, state: ChatState) -> ChatState:
        state.notes = self.note_generator.generate_notes(state.transcript)
        return state
    
    def normal_chat_response(self, state: ChatState) -> ChatState:
        state.notes = "Normal chat response"
        return state