import os
import threading
import nextcord
from nextcord.ext import commands
from flask import Flask

# ----------------------------------------------------------
# 1️⃣  Evitar errores de audio en Python 3.13
# ----------------------------------------------------------
# El módulo 'audioop' fue eliminado en Python 3.13, y nextcord intenta importarlo.
# Esto evita que el bot falle al cargar módulos de voz.
nextcord.opus = None
nextcord.player = None

# ----------------------------------------------------------
# 2️⃣  Configuración del bot
# ----------------------------------------------------------
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------------
# 3️⃣  Evento: cuando el bot se conecta
# ----------------------------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------ Bot is ready and running! ------")

# ----------------------------------------------------------
# 4️⃣  Evento: bienvenida de miembros
# ----------------------------------------------------------
@bot.event
async def on_member_join(member):
    channel_id = int(os.getenv("WELCOME_CHANNEL_ID", 0))
    if not channel_id:
        print("⚠️  No WELCOME_CHANNEL_ID found in environment variables.")
        return
    channel = member.guild.get_channel(channel_id)
    if channel:
        await channel.send(
            f"👋 Welcome to the server, {member.mention}! We're happy to have you here!"
        )
    else:
        print("⚠️  Welcome channel not found.")

# ----------------------------------------------------------
# 5️⃣  Comando básico de ping
# ----------------------------------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! The bot is working correctly.")

# ----------------------------------------------------------
# 6️⃣  Servidor Flask para mantenerlo vivo (Render pings)
# ----------------------------------------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Nuvix Market Bot is alive and running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# ----------------------------------------------------------
# 7️⃣  Lanzar Flask en hilo separado y luego el bot
# ----------------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Missing DISCORD_TOKEN environment variable.")
    else:
        bot.run(token)
