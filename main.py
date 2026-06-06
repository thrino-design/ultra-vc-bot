import os
import asyncio
from pyrogram import Client, filters
from pytube import YouTube
from youtubesearchpython import VideosSearch

# ======================
# ENV VARIABLES
# ======================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ======================
# CLIENT
# ======================
app = Client(
    "vc-bot",
    api_id=39845865,
    api_hash=adf15a3f5aa8103094fab17318f8a041,
    bot_token=8996969044:AAFOE_8S4ISuL7ao_Gdu-MuSLe2a2riAY0Q
)

# ======================
# PYTGCALLS
# ======================
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

call = PyTgCalls(app)

# ======================
# START COMMAND
# ======================
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "✨ 𝗩𝗖 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 🎧\n"
        "━━━━━━━━━━━━━━\n"
        "🤖 Status: Online\n"
        "🎵 /play <song name>\n"
        "⚡ Voice Chat Streaming\n"
        "━━━━━━━━━━━━━━"
    )

# ======================
# PLAY COMMAND
# ======================
@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Give a song name!")

    query = message.text.split(None, 1)[1]

    msg = await message.reply_text("🔎 Searching...")

    search = VideosSearch(query, limit=1).result()["result"]
    if not search:
        return await msg.edit("❌ No results found!")

    url = search[0]["link"]
    title = search[0]["title"]

    await msg.edit(f"🎵 Downloading: {title}")

    yt = YouTube(url)
    stream_url = yt.streams.filter(only_audio=True).first().url

    await msg.edit("🎧 Joining voice chat...")

    try:
        await call.join_group_call(
            message.chat.id,
            AudioPiped(stream_url)
        )
        await msg.edit(f"✅ Now Playing:\n🎶 {title}")
    except Exception as e:
        await msg.edit(f"❌ Error:\n{e}")

# ======================
# START BOT
# ======================
app.start()
call.start()

print("🔥 VC Bot is running...")
idle = asyncio.get_event_loop()
idle.run_forever()
