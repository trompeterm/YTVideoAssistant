from tools.transcript import Transcript
from tools.chunker import Chunker

def main():
    transcript = Transcript()
    chunker = Chunker()
    transcript = transcript.get_transcript("dQw4w9WgXcQ")
    chunks = chunker.chunk_text(transcript, 10)
    print(chunks)

main()