from .state import ChatState
from processors.youtube import YouTubeProcessor
from processors.generator import Generator
from .utils import extract_video_id
import re
from history.chat_history import ChatHistory
from core.openAI import OpenAIAPI
from langchain_core.tools import tool

##tool call
from pathlib import Path
import tempfile
from datetime import datetime
##

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
    
    @tool
    def export_notes(self, notes: str, format: str = "txt") -> str:
        """Export notes to a file
        Args:
            notes (str): The notes to export
            format (str): The format to export the notes in
            
        Returns:
            str: The path to the exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"notes_{timestamp}.{format}"
        
        if format == "txt":
            filename.write_text(notes)
        elif format == "md":
            filename.write_text(notes)
        elif format == "mdx":
            filename.write_text(notes)
        elif format == "pdf":
            self._export_pdf(notes, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return str(filename)
    
    def _export_pdf(self, notes: str, filename: Path):
        from fpdf import FPDF  # Requires `fpdf2` package
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, notes)
        pdf.output(str(filename))
    
    def export_or_respond(self, state: ChatState) -> ChatState:
        """
        Uses the OpenAI LLM to decide whether to export the generated notes
        (via the bound file-export tool) or to simply return them as chat output.
        We then attach a messages list to the state so that the tools_condition
        (which we cannot change) can inspect the last message’s `tool_calls`.
        """
        if not state.notes:
            state.action = "respond"
            state.messages = [Message(role="assistant", content=state.notes, tool_calls=[])]
            return state

        prompt = (
            f"The following notes have been generated:\n\n{state.notes}\n\n"
            "Should these notes be exported as a file (action 'tools') or simply returned "
            "as a chat response (action 'respond')? Please reply with exactly one word: either "
            "'tools' or 'respond'. "
            "Decide based on the user prompt: if the user is requesting to export the notes or "
            "build a pdf or create a markdown file, then return 'tools'; otherwise return 'respond'. "
            f"User prompt: {state.user_input}"
        )
        
        try:
            llm = OpenAIAPI()
            decision = llm.get_response(
                messages=[
                    {"role": "system", "content": "You are a decision-making assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            print("decision:", decision)
            if decision not in ("tools", "respond"):
                decision = "respond"
            state.action = decision
        except Exception as e:
            print(f"LLM decision error: {e}")
            state.action = "respond"
        
        # Attach a messages list so that tools_condition can read the decision.
        # If the decision is "tools", add a non-empty tool_calls list.
        if state.action == "tools":
            tool_call = {"tool": "export_notes", "args": {"notes": state.notes}}
            message = Message(role="assistant", content=state.notes, tool_calls=[tool_call])
        else:
            message = Message(role="assistant", content=state.notes, tool_calls=[])
        
        state.messages = [message]
        return state
