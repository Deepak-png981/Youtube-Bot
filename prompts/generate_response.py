def generate_response_prompt(user_input: str, transcript: str, chat_history: list) -> str:
    system_prompt = (
        "You are a writer that writes high-quality notes with examples and proper explanations from a YouTube video. "
        "We will provide the transcript of the video, and if there is any conversation between the user and the chatbot, "
        "it will also be provided. Generate a response based on the user prompt. "
        f"<Transcript>{transcript}</Transcript> "
        f"<ChatHistory>{chat_history}</ChatHistory> "
    )
    human_prompt = user_input
    return system_prompt, human_prompt
