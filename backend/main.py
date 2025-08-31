from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import numpy as np
from tools.transcript import Transcript
from tools.chunker import Chunker
from tools.embeddings import Embeddings
from tools.chat_completion import ChatCompletion

app = FastAPI()
transcript = Transcript()
chunker = Chunker()
embedder = Embeddings()
chat_completion = ChatCompletion()

video_state = {
    "text": "",
    "chunks": [],
    "vectors": [],
    "index": None,
    "is_processed": False
}

chunk_size = 100

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_video_id(video_link: str) -> str:
    if "=" in video_link:
        return video_link.split("=")[1]
    elif "youtu.be/" in video_link:
        return video_link.split("youtu.be/")[1]
    else:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

@app.post("/process-video")
def process_video(video_link: str):
    """Initialize video processing - gets transcript, chunks, and embeddings"""
    try:
        video_id = get_video_id(video_link)
        text = transcript.get_transcript(video_id)
        chunks = chunker.chunk_text(text, chunk_size)
        vectors = embedder.embed_text(chunks)
        index = embedder.build_index(vectors)
        
        video_state["text"] = text
        video_state["chunks"] = chunks
        video_state["vectors"] = vectors
        video_state["index"] = index
        video_state["is_processed"] = True
        
        return {
            "message": "Video processed successfully",
            "video_id": video_id,
            "chunk_count": len(chunks),
            "text_length": len(text)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

class AskRequest(BaseModel):
    question: str
    message_history: Optional[List[Dict[str, Any]]] = []

@app.post("/ask")
def ask_question(request: AskRequest):
    if not video_state["is_processed"]:
        raise HTTPException(status_code=400, detail="No video has been processed yet. Please call /process-video first.")
    
    try:
        results = embedder.search(request.question, video_state["index"], video_state["chunks"])
        
        # Convert message history to the format expected by chat completion
        history = []
        for msg in request.message_history:
            if msg.get("sender") == "user":
                history.append(f"User: {msg.get('text', '')}")
            elif msg.get("sender") == "assistant":
                history.append(f"Assistant: {msg.get('text', '')}")
        
        # Debug: print the history being sent
        print(f"Debug - History being sent: {history}")
        print(f"Debug - Current question: {request.question}")
        
        response = chat_completion.generate_response(request.question, results, history)
        
        return {
            "question": request.question,
            "answer": response,
            "relevant_chunks_count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
