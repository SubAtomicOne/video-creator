from TTS.api import TTS


class AudioModel:
    def __init__(self, storage_path: str = ""):
        self.storage_path = storage_path
        self.tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True)
        self.speaker = self.tts.speakers[104]

    def generate_audio(self, content: str, filename: str):
        outfile_path = f"{self.storage_path}{filename}.wav"

        self.tts.tts_to_file(
            text=content,
            file_path=outfile_path,
            speaker=self.speaker,
            speed=0.95,
            pitch=0.8,
        )

        print(f"✅ Audio generated! {outfile_path}")

        return outfile_path
