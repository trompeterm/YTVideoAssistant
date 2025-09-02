from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class ChatCompletion:
    def __init__(self):
        self.client = OpenAI()
    
    def generate_response(self, content: str, chunks: list[str], history: list[str]):
        system_content = f"""You are a helpful assistant that can answer questions about the content of the video.

                IMPORTANT: You have access to the conversation history below. You MUST use this history to provide context-aware responses. If the user asks about something mentioned in previous messages, refer to the history.

                You will also be given a list of chunks of the most relevant parts of the transcript.
                You will need to use the chunks to answer the question.

                RELEVANT TRANSCRIPT CHUNKS:
                {chunks}

                CONVERSATION HISTORY:
                {history if history else "No previous conversation history."}

                Remember to use both the conversation history and the transcript chunks to provide accurate, contextual responses.
                If the user mentions "you", they are referring to you, the assistant. If the user says "the speaker", they are referring to the person in the video. 
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": content},
            ]
        )
        return response.choices[0].message.content