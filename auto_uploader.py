from tiktokautouploader import upload_tiktok
import os
import subprocess

# Path to the parent output folder
BASE_DIR = "outputs"

# Get list of all numeric subfolders
subfolders = [f for f in os.listdir(BASE_DIR) if f.isdigit()]
if not subfolders:
    print("No numbered folders found.")
    exit()

# Find the highest-numbered folder
latest_folder = str(max(int(f) for f in subfolders))
#latest_folder = str(79)
video_path = os.path.join(BASE_DIR, latest_folder, "video.mp4")

if not os.path.exists(video_path):
    print(f"No video found at: {video_path}")
    exit()

title_path = os.path.join(BASE_DIR, latest_folder, "title.txt")
description_path = os.path.join(BASE_DIR, latest_folder, "description.txt")

if os.path.exists(title_path):
    with open(title_path, "r") as f:
        video_title = f.read().strip('"')
else:
    video_title = f"AI Story #{latest_folder}"

if os.path.exists(description_path):
    with open(description_path, "r") as f:
        video_description = f.read().strip('"')
else:
    video_description = video_title

print(video_title)
# Call the upload script
subprocess.run([
    "python", "upload_video.py",
    "--file", video_path,
    "--title", video_title,
    "--description", video_description,
    "--keywords", "Fun Fact, AI Stories, Intersting,Tech, Voiceover"
])
try:
    upload_tiktok(
        video=video_path,
        description=video_title,
        accountname='redditcampfirestories'
    )
except Exception as e:
    print(f"[TikTok Upload Error] {e}")
    traceback.print_exc()
