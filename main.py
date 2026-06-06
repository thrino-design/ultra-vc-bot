import os
import asyncio
from collections import defaultdict, deque
from pyrogram import Client, filters
from py_tgcalls import PyTgCalls
from py_tgcalls.types import AudioPiped
from pytube import YouTube
from youtubesearchpython import VideosSearch

# ======================
# ENV VARIABLES
# ======================
API_ID = int(os.getenv("39845865"))
API_HASH = os.getenv("adf15a3f5aa8103094fab17318f8a041")
BOT_TOKEN = os.getenv("8996969044:AAFOE_8S4ISuL7ao_Gdu-MuSLe2a2riAY0Q")

# ======================
# CLIENT + VC SETUP
# ======================
app = Client("ultra-vc-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc = PyTgCalls(app)

# ======================
# STORAGE
# ======================
queues = defaultdict(deque)
playing = {}

# ======================
# YOUTUBE SEARCH
# ======================
def search_song(query):
    search = VideosSearch(query, limit=1)
    result = search.result()["result"][0]
    return result["link"], result["title"]

# ======================
# DOWNLOAD AUDIO
# ======================
def download_audio(link):
    yt = YouTube(link)
    title = yt.title
    file = yt.streams.filter(only_audio=True).first().download(filename="song.mp3")
    return title, file

# ======================
# START COMMAND
# ======================
@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply(
        "🎧 ULTRA VC MUSIC BOT\n\n"
        "Commands:\n"
        "/play <song name or link>\n"
        "/skip\n"
        "/pause\n"
        "/resume\n"
        "/stop"
    )

# ======================
# PLAY COMMAND
# ======================
@app.on_message(filters.command("play"))
async def play(_, msg):
    chat_id = msg.chat.id

    if len(msg.command) < 2:
        return await msg.reply("❌ Send song name or YouTube link")

    query = " ".join(msg.command[1:])

    if "http" not in query:
        link, title = search_song(query)
    else:
        link = query
        title = "YouTube Audio"

    queues[chat_id].append((link, title))

    if not playing.get(chat_id):
        await start_play(chat_id, msg)
    else:
        await msg.reply(f"➕ Added to queue: {title}")

# ======================
# START PLAYBACK
# ======================
async def start_play(chat_id, msg):
    playing[chat_id] = True

    link, title = queues[chat_id].popleft()

    await msg.reply("🔄 Downloading...")

    title, file = download_audio(link)

    await vc.join_group_call(chat_id, AudioPiped(file))

    await msg.reply(f"🎶 Now Playing:\n{title}")

# ======================
# SKIP
# ======================
@app.on_message(filters.command("skip"))
async def skip(_, msg):
    chat_id = msg.chat.id

    try:
        await vc.leave_group_call(chat_id)
    except:
        pass

    if queues[chat_id]:
        await start_play(chat_id, msg)
    else:
        playing[chat_id] = False
        await msg.reply("⏭ Queue empty")

# ======================
# STOP
# ======================
@app.on_message(filters.command("stop"))
async def stop(_, msg):
    chat_id = msg.chat.id

    queues[chat_id].clear()
    playing[chat_id] = False

    try:
        await vc.leave_group_call(chat_id)
    except:
        pass

    await msg.reply("⏹ Stopped & cleared queue")

# ======================
# PAUSE
# ======================
@app.on_message(filters.command("pause"))
async def pause(_, msg):
    await vc.pause_stream(msg.chat.id)
    await msg.reply("⏸ Paused")

# ======================
# RESUME
# ======================
@app.on_message(filters.command("resume"))
async def resume(_, msg):
    await vc.resume_stream(msg.chat.id)
    await msg.reply("▶️ Resumed")

# ======================
# MAIN LOOP
# ======================
async def main():
    await app.start()
    await vc.start()
    print("🔥 ULTRA VC BOT IS RUNNING")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
