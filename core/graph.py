from langgraph.graph import StateGraph, END
from .nodes import GraphNodes, route_input
from .state import ChatState

class ChatGraph:
    def __init__(self):
        self.nodes = GraphNodes()
        self.graph = StateGraph(ChatState)
        self._build_graph()
    
    def _build_graph(self):
        self.graph.add_node("detect_url", self.nodes.detect_youtube_url)
        self.graph.add_node("extract_transcript", self.nodes.extract_transcript)
        self.graph.add_node("generate_notes", self.nodes.generate_notes)
        self.graph.add_node("normal_chat", self.nodes.normal_chat_response)
        
        self.graph.set_conditional_entry_point(
            route_input,
            {
                "youtube_flow": "detect_url",
                "normal_chat": "normal_chat"
            }
        )
        
        self.graph.add_edge("detect_url", "extract_transcript")
        self.graph.add_edge("extract_transcript", "generate_notes")
        
        self.graph.add_edge("generate_notes", END)
        self.graph.add_edge("normal_chat", END)
        
        self.compiled = self.graph.compile()
    
    def execute(self, user_input: str) -> ChatState:
        result = self.compiled.invoke(ChatState(user_input=user_input))
        state = ChatState(**result)
        return state
