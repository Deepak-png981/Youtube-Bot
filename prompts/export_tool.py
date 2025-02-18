def export_tool_prompt(user_input: str, notes: str, history: list[dict]) -> str:
    return (
        "You are a helpful assistant that can analyze the user prompt"
        "Based on the user prompt decide if you want to call the tools or not."
        "Our system is such that we work youtube to notes generation."
        "Our system contains the notes , we can perform various operations on it using the tools."
        "NOTE: If the user prompt contains anything related to the tool call , then we will call the tool only in that case."
        "We will be providing you with the user input and the generated notes."
        "We will be providing you with the chat history till now as well so that you can properly generate the arguments for the tool calls if needed."
        f"<user_input>\n{user_input}\n</user_input>\n"
        f"<notes>\n{notes}\n</notes>\n"
        "Would you like to export these notes to a file? (yes/no)\n"
        "Enter 'yes' to save or 'no' to cancel."
    )
