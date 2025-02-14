from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import whisper
import tempfile
import os
class YouTubeProcessor:
    def __init__(self, use_whisper_fallback=True):
        self.use_whisper = use_whisper_fallback
        self.whisper_model = whisper.load_model("base") if use_whisper_fallback else None

    def get_transcript(self, video_id: str) -> str:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en' , 'en-US'])
            print(f"Transcript: {transcript}")
            return " ".join([t['text'] for t in transcript])
        except Exception as e:
            print("Error in get_transcript: ", e)
            if self.use_whisper:
                return self._fallback_transcript(video_id)
            raise RuntimeError(f"Transcript unavailable: {str(e)}")

    def _fallback_transcript(self, video_id: str) -> str:
        yt = YouTube(f"https://youtu.be/{video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = audio_stream.download(output_path=tmpdir)
            result = self.whisper_model.transcribe(audio_path)
            os.remove(audio_path)
            
        return result["text"]