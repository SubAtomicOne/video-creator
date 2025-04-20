from typing import List, Tuple, Optional
from prefect import flow, task, get_run_logger
import os
import time

# ---- MODELS IMPORTS (assume these are defined somewhere in your code) ----
from models.text import TextModel
from models.image import ImageModel
from models.audio import AudioModel
from models.subtitle import SubtitleModel
from models.video import VideoModel
from decorators import with_manual_approval

STORAGE = "outputs"


@task(retries=0, retry_delay_seconds=5)
def get_content() -> str:
    text_model = TextModel()
    content = text_model.generate_content()
    return content


@with_manual_approval("Are you satisfied with the generated prompts? [y/N]:")
@task(retries=0, retry_delay_seconds=5)
def get_prompts(content) -> List[str]:
    logger = get_run_logger()
    text_model = TextModel()
    prompts = text_model.generate_image_prompts(content)

    logger.info(prompts)

    return prompts


@task(retries=0)
def create_images(prompts: List[str]) -> str:
    image_storage = f"{STORAGE}/images/"
    os.makedirs(image_storage, exist_ok=True)

    image_model = ImageModel(image_storage)
    timestamp = str(time.time())
    image_model.generate_images(prompts, timestamp)

    return image_storage


@task(retries=0)
def create_audio(content: str) -> str:
    audio_storage = f"{STORAGE}/audio/"
    os.makedirs(audio_storage, exist_ok=True)

    audio_model = AudioModel(audio_storage)
    timestamp = str(time.time())
    file_path = audio_model.generate_audio(content, timestamp)

    return file_path


@task
def create_subtitle(audio_filepath: str) -> List:
    subtitle_model = SubtitleModel()
    return subtitle_model.generate_subtitle(audio_filepath)


@task
def create_video(
    audio_path: str,
    image_folder: str,
    subtitle: Optional[List],
    bgm_path: Optional[str],
):
    video_path = f"{STORAGE}/video.mp4"
    video_model = VideoModel(audio_path)
    video_model.set_video(image_folder)
    video_model.attach_audio(bgm_path)
    if subtitle:
        video_model.attach_subtitle(subtitle)
    video_model.generate_video(video_path)


# ---- FLOW ----


@flow(name="content-to-video-pipeline")
def content_to_video_pipeline():
    content = get_content()
    image_prompts = get_prompts(content)
    images_folder = create_images(image_prompts)
    audio_path = create_audio(content)
    subtitle = create_subtitle(audio_path)

    create_video(
        audio_path=audio_path,
        image_folder=images_folder,
        subtitle=subtitle,
        bgm_path="bgms/classic.mp3",
    )


# ---- ENTRY ----

if __name__ == "__main__":
    content_to_video_pipeline()
