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
        print("⚠️ No WELCOME_CHANNEL_ID found in environment variables.")
        return

    channel = member.guild.get_channel(channel_id)
    if not channel:
        print("⚠️ Welcome channel not found.")
        return

    # 📅 Fecha de ingreso formateada
    joined_date = member.joined_at.strftime("%B %d, %Y %H:%M")

    # 💠 Embed con estilo Nebula
    embed = nextcord.Embed(
        title="🎉 A new user has joined!",
        description=(
            f"Hey {member.mention}, welcome to **Nuvix Market 🎃**!\n\n"
            "Explore the server, meet awesome people, and don’t forget to check our rules before starting.\n"
            "We’re happy to have you here 💜"
        ),
        color=nextcord.Color.purple()
    )

    # 💬 Autor del embed
    embed.set_author(
        name=f"Welcome System - Nuvix Market 🎃",
        icon_url="https://cdn.discordapp.com/emojis/1201021237746053161.webp?size=96&quality=lossless"
    )

    # 📸 Miniatura del usuario
    embed.set_thumbnail(url=member.display_avatar.url)

    # 🕒 Campos de información
    embed.add_field(name="👤 User", value=f"{member.mention}", inline=True)
    embed.add_field(name="🕓 Joined On", value=f"{joined_date}", inline=True)

    # 🖼️ Banner de bienvenida
    embed.set_image(url="https://i.imgur.com/fcFxMVA.png")  # Cambia este enlace por tu banner personalizado

    # ✨ Footer
    embed.set_footer(text="Welcome System - Nuvix Market 🎃")

    # Envía el embed
    await channel.send(embed=embed)
    print(f"✅ Sent welcome embed for {member.name}")

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

