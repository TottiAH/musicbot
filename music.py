import os
import random
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1480898961744330803/XaOQtgiWgSepTzsQs_pP-zf69KAv0gtk5EMTFrptO8lh96_zHkqcNpcE8WHQdICohGW3"
API_KEY = os.environ.get("YOUTUBE_API_KEY")


def get_random_music():
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": "hip hop chill music",
        "type": "video",
        "videoCategoryId": "10",
        "maxResults": 25,
        "regionCode": "US",
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        return None, f"YouTube API error {response.status_code}: {response.text[:300]}"

    data = response.json()
    items = data.get("items", [])

    if not items:
        return None, "items が 0 件だった"

    video = random.choice(items)

    title = video["snippet"]["title"]
    video_id = video["id"]["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return (title, video_url), None


if not API_KEY:
    message = {
        "content": "YOUTUBE_API_KEY が読めてない"
    }
else:
    song, error = get_random_music()

    if error:
        message = {
            "content": error
        }
    elif song:
        title, url = song
        message = {
            "content": f"🎧 今日の音楽\n\n**{title}**\n{url}"
        }
    else:
        message = {
            "content": "原因不明で song が取れなかった"
        }

requests.post(WEBHOOK_URL, json=message, timeout=20)
