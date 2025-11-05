import os
import re
import time
from pathlib import Path
from datetime import datetime
import yt_dlp

# -----------------------------
# Config
# -----------------------------
CONFIG_PATH = Path("/data/config/urls.txt")
DOWNLOADS_PATH = Path("/data/downloads")
LOGS_PATH = Path("/data/logs")

MAX_PER_DAY = int(os.getenv("MAX_PER_DAY", 5))
DELAY_HOURS = float(os.getenv("DELAY_HOURS", 4))

ARCHIVE_FILE = DOWNLOADS_PATH / ".downloaded.txt"
ARCHIVE_FILE.touch(exist_ok=True)

# -----------------------------
# Helper Functions
# -----------------------------
def normalize_name(name: str, lowercase=True, trim=True) -> str:
    """Normalize folder/filename."""
    name = re.sub(r"[^0-9a-zA-Z]+", "-", name)
    name = re.sub(r"-{2,}", "-", name)
    if lowercase:
        name = name.lower()
    if trim:
        name = name.strip("-")
    return name

def load_urls():
    """Load URLs from urls.txt."""
    if not CONFIG_PATH.exists():
        return []
    with open(CONFIG_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return lines

def load_downloaded():
    """Load list of already downloaded video IDs."""
    with open(ARCHIVE_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_downloaded(video_id):
    """Mark video as downloaded."""
    with open(ARCHIVE_FILE, "a") as f:
        f.write(video_id + "\n")

def get_video_id(info):
    return info.get("id")

# -----------------------------
# Main Download Function
# -----------------------------
def download_video(url):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": str(DOWNLOADS_PATH / "%(playlist_title)s" / "%(upload_date)s - %(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "noplaylist": False,
        "download_archive": str(ARCHIVE_FILE),
        "writesubtitles": False,
        "progress_hooks": [],
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info

# -----------------------------
# Scheduler
# -----------------------------
def main():
    while True:
        urls = load_urls()
        downloaded_set = load_downloaded()
        videos_to_download = []

        # Expand playlists into individual videos
        for url in urls:
            try:
                with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if "entries" in info:
                        for entry in info["entries"]:
                            if entry["id"] not in downloaded_set:
                                videos_to_download.append(entry["webpage_url"])
                    else:
                        if info["id"] not in downloaded_set:
                            videos_to_download.append(url)
            except Exception as e:
                print(f"[{datetime.now()}] Failed to extract {url}: {e}")

        if not videos_to_download:
            print(f"[{datetime.now()}] No new videos to download. Checking again in 10 minutes...")
            time.sleep(600)
            continue

        # Download up to MAX_PER_DAY videos
        for i, video_url in enumerate(videos_to_download[:MAX_PER_DAY]):
            print(f"[{datetime.now()}] Starting download ({i+1}/{len(videos_to_download)}): {video_url}")
            try:
                info = download_video(video_url)
                vid_id = get_video_id(info)
                if vid_id:
                    save_downloaded(vid_id)
            except Exception as e:
                print(f"[{datetime.now()}] Error downloading {video_url}: {e}")

            print(f"[{datetime.now()}] Sleeping for {DELAY_HOURS} hours before next download...")
            time.sleep(DELAY_HOURS * 3600)

        # Check again after finishing daily batch
        print(f"[{datetime.now()}] Finished batch. Will check for new URLs shortly.")
        time.sleep(600)  # check every 10 minutes for new URLs

if __name__ == "__main__":
    DOWNLOADS_PATH.mkdir(parents=True, exist_ok=True)
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    main()
