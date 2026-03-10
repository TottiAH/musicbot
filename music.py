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
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("YouTube API error")
        return None

    data = response.json()

    items = data.get("items", [])

    if not items:
        return None

    video = random.choice(items)

    title = video["snippet"]["title"]
    video_id = video["id"]["videoId"]

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return title, video_url


song = get_random_music()

if song:
    title, url = song

    message = {
        "content": f"🎧 今日の音楽\n\n**{title}**\n{url}"
    }

else:
    message = {
        "content": "音楽が見つからなかった"
    }

requests.post(WEBHOOK_URL, json=message)
