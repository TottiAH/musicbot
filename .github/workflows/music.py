import random
import subprocess
import json
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1480898961744330803/XaOQtgiWgSepTzsQs_pP-zf69KAv0gtk5EMTFrptO8lh96_zHkqcNpcE8WHQdICohGW3"

def get_random_song():
    cmd = [
        "yt-dlp",
        "ytsearch10:music",
        "--dump-single-json",
        "--skip-download"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)

    entries = data.get("entries", [])
    if not entries:
        return None

    video = random.choice(entries)

    title = video.get("title", "タイトル不明")
    url = video.get("webpage_url", "")

    return title, url


song = get_random_song()

if song:
    title, url = song

    message = {
        "content": f"🔥 今日の音楽\n**{title}**\n{url}"
    }

    requests.post(WEBHOOK_URL, json=message)

else:
    requests.post(WEBHOOK_URL, json={"content": "音楽が見つからなかった"})v
