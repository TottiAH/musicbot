import discord
import random
import subprocess
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "MTQ4MDQ3Nzk0MTczNjUzODExMw.GgQlHM.gMqLGbSelcLJZ5HGA2PQ9rxu_iCZkR6KjPjmEo"
CHANNEL_NAME = "トーク"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_random_youtube_song():
    cmd = [
        "yt-dlp",
        "ytsearch10:music",
        "--dump-single-json",
        "--skip-download"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    data = json.loads(result.stdout)

    entries = data.get("entries", [])
    if not entries:
        return None

    video = random.choice(entries)
    title = video.get("title", "タイトル不明")
    url = video.get("webpage_url", "")
    return title, url

async def post_music():
    print("post_music 発火")
    await client.wait_until_ready()

    for guild in client.guilds:
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

        if channel:
            await channel.send("🔥 発火した")
            try:
                song = get_random_youtube_song()
                if not song:
                    await channel.send("🎧 今日の音楽\n\n検索結果が見つからなかった")
                    return

                title, url = song
                await channel.send(f"🎧 今日の音楽\n\n**{title}**\n{url}")

            except Exception as e:
                await channel.send(f"⚠️ 音楽取得エラー: {e}")

@client.event
async def on_ready():
    print("BOT起動:", client.user)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_music, "cron", hour=21, minute=00)
    scheduler.start()
client.run(TOKEN)