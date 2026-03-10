import random
import subprocess
import json
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1480898961744330803/XaOQtgiWgSepTzsQs_pP-zf69KAv0gtk5EMTFrptO8lh96_zHkqcNpcE8WHQdICohGW3"

def get_random_song():

    cmd = [
        "yt-dlp",
        "ytsearch:music",
        "--get-title",
        "--get-id"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    lines = result.stdout.strip().split("\n")

    if len(lines) < 2:
        return None

    title = lines[0]
    video_id = lines[1]

    url = f"https://www.youtube.com/watch?v={video_id}"

    return title, url

song = get_random_song()

if song:
    title, url = song
    message = {
        "content": f"🎵 今日の音楽\n**{title}**\n{url}"
    }
else:
    message = {
        "content": "音楽が見つからなかった"
    }

requests.post(WEBHOOK_URL, json=message)
