from TTS.api import TTS
#from models.streamlabs_polly import StreamlabsPolly
from kokoro import KPipeline
import soundfile as sf

class AudioModel:
    def __init__(self, storage_path: str = "", lang_code: str = 'a', voice: str = 'af_heart'):
        self.storage_path = storage_path
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice = voice

    def generate_audio(self, content: str, filename: str, speed: float = 1.0):
        outfile = f"{self.storage_path}{filename}.wav"
        # Generate and write audio in one pass
        generator = self.pipeline(content, voice=self.voice, speed=speed, split_pattern=r'\n+')

        audio_data = []
        samplerate = None
        for _, _, audio in generator:
            audio_data.append(audio)
            samplerate = 24000  
        import numpy as np
        audio_all = np.concatenate(audio_data, axis=0)
        sf.write(outfile, audio_all, samplerate)
        print(f"✅ Kokoro audio generated: {outfile}")
        return outfile

class OldAudioModel:
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
