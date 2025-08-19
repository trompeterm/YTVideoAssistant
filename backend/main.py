from tools.transcript import Transcript
from tools.chunker import Chunker
from tools.embeddings import Embeddings

def main():
    transcript = Transcript()
    chunker = Chunker()
    embedder = Embeddings()
    text = transcript.get_transcript("dQw4w9WgXcQ")
    chunks = chunker.chunk_text(text, 10)
    vectors = embedder.embed_text(chunks)
    index = embedder.build_index(vectors)
    results = embedder.search("What does the singer say he will never do?", index, chunks)
    print(results)

main()