import random
import subprocess
import json
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1480898961744330803/XaOQtgiWgSepTzsQs_pP-zf69KAv0gtk5EMTFrptO8lh96_zHkqcNpcE8WHQdICohGW3"

def get_random_song():
    cmd = [
        "yt-dlp",
        "ytsearch20:music",
        "--dump-single-json",
        "--skip-download",
        "--default-search", "ytsearch"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("yt-dlp error:", result.stderr)
        return None

    if not result.stdout.strip():
        print("yt-dlp returned empty stdout")
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("json decode error:", e)
        print(result.stdout[:500])
        return None

    entries = data.get("entries", [])
    entries = [e for e in entries if isinstance(e, dict)]

    if not entries:
        print("No valid entries found")
        return None

    video = random.choice(entries)

    title = video.get("title", "タイトル不明")
    url = video.get("webpage_url") or video.get("url")

    if not url:
        return None

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
