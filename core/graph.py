from langgraph.graph import StateGraph, END
from .nodes import GraphNodes, route_input
from .state import ChatState
from langgraph.prebuilt import ToolNode, tools_condition
from processors.file_export import FileExporter
class ChatGraph:
    def __init__(self):
        self.nodes = GraphNodes()
        self.graph = StateGraph(ChatState)
        self.file_exporter = FileExporter()
        self._build_graph()
    
    def _build_graph(self):
        
        tools_node = ToolNode([self.nodes.export_notes])

        self.graph.add_node("detect_url", self.nodes.detect_youtube_url)
        self.graph.add_node("extract_transcript", self.nodes.extract_transcript)
        self.graph.add_node("generate_notes", self.nodes.generate_notes)
        self.graph.add_node("normal_chat", self.nodes.normal_chat_response)
        self.graph.add_node("export_or_respond", self.nodes.export_or_respond)
        self.graph.add_node("tools", tools_node)
        
        self.graph.set_conditional_entry_point(
            route_input,
            {
                "youtube_flow": "detect_url",
                "normal_chat": "normal_chat"
            }
        )
        
        self.graph.add_edge("detect_url", "extract_transcript")
        self.graph.add_edge("extract_transcript", "generate_notes")
        
        self.graph.add_edge("generate_notes", "export_or_respond")
        self.graph.add_edge("normal_chat", "export_or_respond")
        self.graph.add_conditional_edges(
            "export_or_respond",
            should_export,
            {
                "tools": "tools",
                "__end__": END
            }
        )
        self.graph.add_edge("tools", END)
        
        self.compiled = self.graph.compile()
    
    def execute(self, user_input: str) -> ChatState:
        result = self.compiled.invoke(ChatState(user_input=user_input))
        state = ChatState(**result)
        return state
