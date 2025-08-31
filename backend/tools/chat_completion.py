from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class ChatCompletion:
    def __init__(self):
        self.client = OpenAI()
    
    def generate_response(self, content: str, chunks: list[str], history: list[str]):
        # Debug: print what we're receiving
        print(f"Debug - Chat completion received:")
        print(f"  Content: {content}")
        print(f"  History length: {len(history)}")
        print(f"  History: {history}")
        print(f"  Chunks length: {len(chunks)}")
        
        # Format the system message with actual values
        system_content = f"""You are a helpful assistant that can answer questions about the content of the video.

IMPORTANT: You have access to the conversation history below. You MUST use this history to provide context-aware responses. If the user asks about something mentioned in previous messages, refer to the history.

You will also be given a list of chunks of the most relevant parts of the transcript.
You will need to use the chunks to answer the question.

CONVERSATION HISTORY:
{history if history else "No previous conversation history."}

RELEVANT TRANSCRIPT CHUNKS:
{chunks}

Remember to use both the conversation history and the transcript chunks to provide accurate, contextual responses.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": content},
            ]
        )
        return response.choices[0].message.content