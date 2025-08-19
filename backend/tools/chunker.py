class Chunker:
    def __init__(self):
        pass

    def chunk_text(self, text: str, chunk_size: int):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i+chunk_size]))
        return chunks