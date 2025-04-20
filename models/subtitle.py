import whisperx
from typing import List


class SubtitleModel:
    def __init__(self):
        self.model = whisperx.load_model("medium", device="cpu", compute_type="float32")

    def generate_subtitle(self, audio_filepath: str) -> List:
        result = self.model.transcribe(audio_filepath)
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"], device="cpu"
        )
        aligned = whisperx.align(
            result["segments"], model_a, metadata, audio_filepath, device="cpu"
        )

        print("✅ Subtitles generated!")

        subtitle = []
        for word_data in aligned["word_segments"]:
            subtitle.append(word_data)

        return subtitle
