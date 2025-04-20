from models.text import TextModel
from models.image import ImageModel
from models.audio import AudioModel
from models.subtitle import SubtitleModel
from models.video import VideoModel
import util
import os
from typing import List, Tuple, Optional
import time
import random


def get_output_path() -> str:
    def get_video_number() -> int:
        file_path = "database/video_count.txt"
        data = util.read_file(file_path)
        count = 1
        if data:
            count = int(data)

        util.write_file(str(count + 1), file_path)

        return count

    n = get_video_number()
    output_path = f"outputs/{n}"

    os.makedirs(output_path, exist_ok=True)

    return output_path


STORAGE = get_output_path()


DEFAULT_TOPICS = [
    "a historical inspiring fact that changed computer science",
    "an ancient story about a clever king or warrior",
    "a strange or funny fact from world history",
    "a scientific discovery that changed human life",
    "a breakthrough in medical science that saved millions",
    "a dramatic moment from World War 1 or World War 2",
    "a surprising origin of a modern invention",
    "a fun random fact that will make people smile",
    # "a tech innovation that shaped the digital world",
    # "a programming tip that can improve your workflow",
    # "best practices for clean and maintainable code",
    # "essential software architecture techniques every developer should know",
    # "how to build scalable and efficient software systems",
    # "tips for parents on supporting children's learning at home",
    # "how to motivate students for effective study habits",
]


def get_content() -> Tuple[str, List[str]]:
    text_model = TextModel()
    topic = random.choice(DEFAULT_TOPICS)
    # topic = DEFAULT_TOPICS[9]
    content = text_model.generate_content(topic)
    content_storage = f"{STORAGE}/content/"
    os.makedirs(content_storage)
    util.write_file(content, f"{content_storage}content.txt")
    prompts = text_model.generate_image_prompts(content)
    util.write_file(str(prompts), f"{content_storage}prompts.json")

    return (content, prompts)


def create_images(prompts: List[str]) -> str:
    image_storage = f"{STORAGE}/images/"
    os.makedirs(image_storage)

    image_model = ImageModel(image_storage)
    timestamp = str(time.time())

    image_model.generate_images(prompts, timestamp)

    return image_storage


def create_audio(content: str) -> str:
    audio_storage = f"{STORAGE}/audio/"
    os.makedirs(audio_storage, exist_ok=True)

    audio_model = AudioModel(audio_storage)
    timestamp = str(time.time())
    file_path = audio_model.generate_audio(content, timestamp)

    return file_path


def create_subtitle(audio_filepath: str) -> List:
    subtitle_model = SubtitleModel()
    return subtitle_model.generate_subtitle(audio_filepath)


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


def main():
    content, image_prompts = get_content()

    audio_path = create_audio(content)

    subtitle = create_subtitle(audio_path)

    images_folder = create_images(image_prompts)

    create_video(
        audio_path=audio_path,
        image_folder=images_folder,
        subtitle=subtitle,
        bgm_path="bgms/classic.mp3",
    )


# Sample

# subtitle = [
#     {"word": "Welcome", "start": 0.031, "end": 0.411, "score": 0.683},
#     {"word": "to", "start": 0.472, "end": 0.552, "score": 0.956},
#     {"word": "the", "start": 0.592, "end": 0.652, "score": 0.959},
#     {"word": "channel.", "start": 0.692, "end": 0.992, "score": 0.895},
#     {"word": "Did", "start": 1.152, "end": 1.272, "score": 0.887},
#     {"word": "you", "start": 1.293, "end": 1.373, "score": 0.619},
#     {"word": "know", "start": 1.393, "end": 1.493, "score": 0.851},
#     {"word": "that", "start": 1.533, "end": 1.633, "score": 0.75},
#     {"word": "the", "start": 1.673, "end": 1.733, "score": 0.978},
#     {"word": "first", "start": 1.793, "end": 1.993, "score": 0.933},
#     {"word": "mouse", "start": 2.053, "end": 2.274, "score": 0.949},
#     {"word": "was", "start": 2.314, "end": 2.414, "score": 0.932},
#     {"word": "actually", "start": 2.534, "end": 2.814, "score": 0.902},
#     {"word": "designed", "start": 2.874, "end": 3.255, "score": 0.927},
#     {"word": "by", "start": 3.335, "end": 3.415, "score": 0.975},
#     {"word": "Douglas", "start": 3.455, "end": 3.856, "score": 0.708},
#     {"word": "Engelbart", "start": 3.916, "end": 4.276, "score": 0.869},
#     {"word": "in", "start": 4.316, "end": 4.356, "score": 0.629},
#     {"word": "1964,", "start": 4.376, "end": 5.117, "score": 0.88},
#     {"word": "not", "start": 5.558, "end": 5.738, "score": 0.892},
#     {"word": "Apple", "start": 5.878, "end": 6.098, "score": 0.622},
#     {"word": "co-founder", "start": 6.118, "end": 7.019, "score": 0.9},
#     {"word": "Steve", "start": 7.059, "end": 7.34, "score": 0.708},
#     {"word": "Jobs", "start": 7.38, "end": 7.66, "score": 0.857},
#     {"word": "as", "start": 7.76, "end": 7.82, "score": 0.872},
#     {"word": "many", "start": 7.88, "end": 8.081, "score": 0.878},
#     {"word": "people", "start": 8.121, "end": 8.401, "score": 0.767},
#     {"word": "believe?", "start": 8.441, "end": 8.741, "score": 0.808},
#     {"word": "The", "start": 9.422, "end": 9.502, "score": 0.805},
#     {"word": "first", "start": 9.542, "end": 9.763, "score": 0.884},
#     {"word": "public", "start": 9.843, "end": 10.143, "score": 0.866},
#     {"word": "demonstration", "start": 10.183, "end": 10.804, "score": 0.859},
#     {"word": "of", "start": 10.864, "end": 10.904, "score": 0.994},
#     {"word": "the", "start": 10.944, "end": 11.004, "score": 0.995},
#     {"word": "mouse", "start": 11.024, "end": 11.284, "score": 0.815},
#     {"word": "took", "start": 11.304, "end": 11.465, "score": 0.883},
#     {"word": "place", "start": 11.525, "end": 11.745, "score": 0.946},
#     {"word": "at", "start": 11.825, "end": 11.865, "score": 0.886},
#     {"word": "Stanford", "start": 11.925, "end": 12.266, "score": 0.876},
#     {"word": "Research", "start": 12.286, "end": 12.666, "score": 0.817},
#     {"word": "Institute,", "start": 12.726, "end": 13.187, "score": 0.865},
#     {"word": "where", "start": 13.407, "end": 13.567, "score": 0.794},
#     {"word": "Engelbart's", "start": 13.587, "end": 14.048, "score": 0.667},
#     {"word": "ShowTag", "start": 14.068, "end": 14.508, "score": 0.801},
#     {"word": "could", "start": 14.548, "end": 14.689, "score": 0.962},
#     {"word": "be", "start": 14.709, "end": 14.789, "score": 0.992},
#     {"word": "used", "start": 14.909, "end": 15.069, "score": 0.798},
#     {"word": "to", "start": 15.109, "end": 15.169, "score": 0.996},
#     {"word": "control", "start": 15.229, "end": 15.489, "score": 0.851},
#     {"word": "a", "start": 15.55, "end": 15.57, "score": 0.571},
#     {"word": "cursor", "start": 15.63, "end": 15.95, "score": 0.731},
#     {"word": "on", "start": 16.05, "end": 16.11, "score": 0.98},
#     {"word": "a", "start": 16.15, "end": 16.17, "score": 0.897},
#     {"word": "computer", "start": 16.23, "end": 16.631, "score": 0.767},
#     {"word": "screen.", "start": 16.671, "end": 16.931, "score": 0.844},
#     {"word": "Can", "start": 17.572, "end": 17.692, "score": 0.893},
#     {"word": "you", "start": 17.732, "end": 17.832, "score": 0.831},
#     {"word": "imagine", "start": 17.892, "end": 18.233, "score": 0.989},
#     {"word": "using", "start": 18.333, "end": 18.553, "score": 0.934},
#     {"word": "computers", "start": 18.573, "end": 19.014, "score": 0.802},
#     {"word": "without", "start": 19.034, "end": 19.294, "score": 0.86},
#     {"word": "mice", "start": 19.354, "end": 19.554, "score": 0.766},
#     {"word": "or", "start": 19.634, "end": 19.695, "score": 0.875},
#     {"word": "trackpads?", "start": 19.735, "end": 20.275, "score": 0.846},
#     {"word": "It's", "start": 21.036, "end": 21.156, "score": 0.558},
#     {"word": "hard", "start": 21.216, "end": 21.377, "score": 0.71},
#     {"word": "to", "start": 21.417, "end": 21.497, "score": 0.77},
#     {"word": "think", "start": 21.537, "end": 21.697, "score": 0.805},
#     {"word": "about", "start": 21.737, "end": 21.917, "score": 0.902},
#     {"word": "now.", "start": 21.977, "end": 22.198, "score": 0.809},
#     {"word": "But", "start": 22.898, "end": 23.018, "score": 0.91},
#     {"word": "what's", "start": 23.039, "end": 23.239, "score": 0.901},
#     {"word": "even", "start": 23.279, "end": 23.579, "score": 0.73},
#     {"word": "funnier", "start": 23.639, "end": 23.94, "score": 0.952},
#     {"word": "is", "start": 24.02, "end": 24.08, "score": 0.94},
#     {"word": "that", "start": 24.12, "end": 24.24, "score": 0.96},
#     {"word": "Engelbart", "start": 24.3, "end": 24.741, "score": 0.753},
#     {"word": "was", "start": 24.781, "end": 24.901, "score": 0.646},
#     {"word": "rejected", "start": 24.961, "end": 25.341, "score": 0.85},
#     {"word": "27", "start": 25.361, "end": 25.702, "score": 0.724},
#     {"word": "times", "start": 26.062, "end": 26.342, "score": 0.948},
#     {"word": "before", "start": 26.403, "end": 26.663, "score": 0.971},
#     {"word": "he", "start": 26.723, "end": 26.803, "score": 0.804},
#     {"word": "got", "start": 26.863, "end": 27.023, "score": 0.969},
#     {"word": "his", "start": 27.063, "end": 27.183, "score": 0.887},
#     {"word": "project", "start": 27.244, "end": 27.584, "score": 0.793},
#     {"word": "funded.", "start": 27.604, "end": 28.485, "score": 0.975},
#     {"word": "Today,", "start": 28.465, "end": 28.826, "score": 0.886},
#     {"word": "we", "start": 28.846, "end": 29.006, "score": 0.722},
#     {"word": "use", "start": 29.126, "end": 29.226, "score": 0.983},
#     {"word": "mice", "start": 29.266, "end": 29.487, "score": 0.986},
#     {"word": "in", "start": 29.547, "end": 29.607, "score": 0.99},
#     {"word": "every", "start": 29.687, "end": 29.847, "score": 0.977},
#     {"word": "kind", "start": 29.888, "end": 30.088, "score": 0.87},
#     {"word": "of", "start": 30.108, "end": 30.168, "score": 0.75},
#     {"word": "device", "start": 30.188, "end": 30.529, "score": 0.887},
#     {"word": "laptops,", "start": 30.589, "end": 31.09, "score": 0.948},
#     {"word": "desktops,", "start": 31.23, "end": 31.691, "score": 0.726},
#     {"word": "tablets,", "start": 31.711, "end": 32.412, "score": 0.853},
#     {"word": "and", "start": 32.432, "end": 32.512, "score": 0.987},
#     {"word": "smartphones.", "start": 32.572, "end": 33.173, "score": 0.83},
#     {"word": "The", "start": 33.935, "end": 34.035, "score": 0.779},
#     {"word": "impact", "start": 34.095, "end": 34.496, "score": 0.924},
#     {"word": "of", "start": 34.516, "end": 34.556, "score": 0.498},
#     {"word": "Engelbert's", "start": 34.676, "end": 35.197, "score": 0.814},
#     {"word": "invention", "start": 35.257, "end": 35.678, "score": 0.899},
#     {"word": "on", "start": 35.778, "end": 35.838, "score": 0.928},
#     {"word": "computer", "start": 35.918, "end": 36.359, "score": 0.955},
#     {"word": "science", "start": 36.379, "end": 36.659, "score": 0.851},
#     {"word": "is", "start": 36.76, "end": 36.82, "score": 0.857},
#     {"word": "undeniable.", "start": 36.9, "end": 37.401, "score": 0.864},
#     {"word": "His", "start": 38.102, "end": 38.222, "score": 0.729},
#     {"word": "work", "start": 38.262, "end": 38.423, "score": 0.985},
#     {"word": "laid", "start": 38.463, "end": 38.623, "score": 0.845},
#     {"word": "the", "start": 38.663, "end": 38.743, "score": 0.803},
#     {"word": "foundation", "start": 38.803, "end": 39.284, "score": 0.862},
#     {"word": "for", "start": 39.344, "end": 39.444, "score": 0.906},
#     {"word": "modern", "start": 39.484, "end": 39.765, "score": 0.693},
#     {"word": "user", "start": 39.845, "end": 40.085, "score": 0.903},
#     {"word": "interfaces.", "start": 40.126, "end": 40.707, "score": 0.939},
#     {"word": "Like,", "start": 41.548, "end": 41.788, "score": 0.991},
#     {"word": "share,", "start": 41.869, "end": 42.109, "score": 0.651},
#     {"word": "and", "start": 42.129, "end": 42.209, "score": 0.752},
#     {"word": "subscribe", "start": 42.249, "end": 42.73, "score": 0.837},
#     {"word": "to", "start": 42.79, "end": 42.87, "score": 0.952},
#     {"word": "learn", "start": 42.91, "end": 43.091, "score": 0.674},
#     {"word": "more", "start": 43.131, "end": 43.291, "score": 0.847},
#     {"word": "funny", "start": 43.351, "end": 43.552, "score": 0.867},
#     {"word": "facts", "start": 43.592, "end": 43.832, "score": 0.853},
#     {"word": "that", "start": 43.892, "end": 44.052, "score": 0.944},
#     {"word": "changed", "start": 44.133, "end": 44.413, "score": 0.965},
#     {"word": "our", "start": 44.473, "end": 44.553, "score": 0.999},
#     {"word": "world.", "start": 44.593, "end": 45.495, "score": 0.837},
# ]

# content = """
#     Welcome to the channel, Did you know that the first mouse was actually designed by Douglas Engelbart in 1964, not Apple co-founder Steve Jobs as many people believe! The first public demonstration of the mouse took place at Stanford Research Institute, where Engelbart showed how it could be used to control a cursor on a computer screen. Can you imagine using computers without mice or trackpads? It's hard to think about now! But what's even funnier is that Engelbart was rejected 27 times before he got his project funded. Today, we use mice in every kind of device - laptops, desktops, tablets, and smartphones! The impact of Engelbart's invention on computer science is undeniable. His work laid the foundation for modern user interfaces.

#     Like, share and subscribe to learn more funny facts that changed our world!
#     """
# images_folder = "../image_generation/images"
# audio_path = "outputs/1/audio/1744046279.984187.wav"

# create_video(
#     audio_path=audio_path,
#     image_folder=images_folder,
#     subtitle=subtitle,
#     bgm_path="bgms/classic.mp3",
# )

main()
