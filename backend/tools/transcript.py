from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

def get_transcript(id: str):
    transcript = ytt_api.fetch(id)
    text = " ".join([entry.text for entry in transcript])
    return text

print(get_transcript("dQw4w9WgXcQ"))