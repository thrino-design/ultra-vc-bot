k	mport os
import asyncio
from pyrogram import Client, filters
from youtubesearchpython import VideosSearch
from pytube import YouTube

# ======================
# ENV
# ======================
API_ID = int(os.getenv("39845865"))
API_HASH = os.getenv("adf15a3f5aa8103094fab17318f8a041")
BOT_TOKEN = os.getenv("8996969044:AAFOE_8S4ISuL7ao_Gdu-MuSLe2a2riAY0Q")

# ======================
# CLIENT
# ======================
app = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ======================
# START
# ======================
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "🎧 𝗩𝗖 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧\n"
        "━━━━━━━━━━━━━━\n"
        "🤖 Status: Online\n"
        "🎵 /play <song name>\n"
        "🔎 YouTube search enabled\n"
        "━━━━━━━━━━━━━━"
    )

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
