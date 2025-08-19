from youtube_transcript_api import YouTubeTranscriptApi

class Transcript:
    def __init__(self):
        self.ytt_api = YouTubeTranscriptApi()

    def get_transcript(self, id: str):
        transcript = self.ytt_api.fetch(id)
        text = " ".join([entry.text for entry in transcript])
        return text