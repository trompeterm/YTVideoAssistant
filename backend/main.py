from tools.transcript import Transcript
from tools.chunker import Chunker
from tools.embeddings import Embeddings
from tools.chat_completion import ChatCompletion

def main():
    transcript = Transcript()
    chunker = Chunker()
    embedder = Embeddings()
    chat_completion = ChatCompletion()
    text = transcript.get_transcript("LPZh9BOjkQs")
    chunks = chunker.chunk_text(text, 100)
    vectors = embedder.embed_text(chunks)
    index = embedder.build_index(vectors)
    results = embedder.search("What are large language models and how do they work?", index, chunks)
    response = chat_completion.generate_response("What are large language models and how do they work?", results, [])
    print(response)

main()