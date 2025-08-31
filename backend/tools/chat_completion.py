from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class ChatCompletion:
    def __init__(self):
        self.client = OpenAI()
    
    def generate_response(self, content: str, chunks: list[str], history: list[str]):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": """You are a helpful assistant that can answer questions about the content of the video.
                 You will also be given a list of chunks of the most relecant pars of the transcript.
                 You will need to use the chunks to answer the question.
                 You will also be given a list of history of the conversation.
                 You may need to use the history to answer the question.
                 
                 Transcript chunks: {chunks}
                 History: {history}
                 """},
                {"role": "user", "content": content},
            ]
        )
        return response.choices[0].message.content