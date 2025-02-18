from langgraph.graph import StateGraph, END
from .nodes import GraphNodes, route_input
from .state import ChatState
from langgraph.prebuilt import ToolExecutor, ToolNode, tools_condition
from processors.tools import export_notes

class ChatGraph:
    def __init__(self):
        self.nodes = GraphNodes()
        self.graph = StateGraph(ChatState)
        self.tool_executor = ToolExecutor([export_notes])  
        self._build_graph()
    
    def _build_graph(self):
        
        tools_node = ToolNode([export_notes])

        self.graph.add_node("detect_url", self.nodes.detect_youtube_url)
        self.graph.add_node("extract_transcript", self.nodes.extract_transcript)
        self.graph.add_node("generate_notes", self.nodes.generate_notes)
        self.graph.add_node("normal_chat", self.nodes.normal_chat_response)
        self.graph.add_node("should_export", self.nodes.should_export)
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
        
        self.graph.add_edge("generate_notes", END)
        self.graph.add_edge("normal_chat", "should_export")
        self.graph.add_conditional_edges("should_export", tools_condition)
        

        self.graph.add_edge("tools", END)
        self.compiled = self.graph.compile()

    def execute(self, user_input: str) -> ChatState:
        result = self.compiled.invoke(ChatState(user_input=user_input, messages=[]))
        state = ChatState(**result)
        return state