import os
import asyncio
from pyrogram import Client, filters
from youtubesearchpython import VideosSearch
from pytube import YouTube

# ======================
# ENV VARIABLES (Render)
# ======================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ======================
# CLIENT
# ======================
app = Client(
    "music-bot",
    api_id=39845865,
    api_hash=adf15a3f5aa8103094fab17318f8a041,
    bot_token=8996969044:AAFOE_8S4ISuL7ao_Gdu-MuSLe2a2riAY0Q
)

# ======================
# START COMMAND
# ======================
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗠𝘂𝘀𝗶𝗰 𝗩𝗖 𝗕𝗼𝘁 🎧\n"
        "━━━━━━━━━━━━━━\n"
        "🤖 Status: Online\n"
        "🎵 Use /play to stream music\n"
        "⚡ Fast & stable VC support\n"
    )

# ======================
# RUN BOT
# ======================


# ======================
# PLAY (DOWNLOAD AUDIO LINK)
# ======================
@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Give a song name!")

    query = message.text.split(None, 1)[1]

    msg = await message.reply_text("🔎 Searching...")

    try:
        search = VideosSearch(query, limit=1).result()["result"]
        if not search:
            return await msg.edit("❌ No results found!")

        url = search[0]["link"]
        title = search[0]["title"]

        await msg.edit(f"🎵 Found:\n{title}\n\n⬇️ Getting audio...")

        yt = YouTube(url)
        stream_url = yt.streams.filter(only_audio=True).first().url

        await msg.edit(
            "⚠️ VC streaming removed (safe version)\n\n"
            f"🎶 Song Ready:\n{title}\n\n"
            "👉 You can upgrade to full VC version later"
        )

    except Exception as e:
        await msg.edit(f"❌ Error:\n{e}")

# ======================
# RUN
# ======================
print("🔥 Bot Started")
app.run()
