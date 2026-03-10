import subprocess
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1480898961744330803/XaOQtgiWgSepTzsQs_pP-zf69KAv0gtk5EMTFrptO8lh96_zHkqcNpcE8WHQdICohGW3"

def get_song():
    cmd = [
        "yt-dlp",
        "ytsearch1:music",
        "--print", "%(title)s",
        "--print", "https://www.youtube.com/watch?v=%(id)s",
        "--skip-download"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("yt-dlp error:")
        print(result.stderr)
        return None

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    if len(lines) < 2:
        print("stdout was:")
        print(result.stdout)
        return None

    title = lines[0]
    url = lines[1]
    return title, url


song = get_song()

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
