# --- FIX para Python 3.13 ---
# Crea un módulo falso para "audioop" para evitar el error.
import sys, types
sys.modules['audioop'] = types.ModuleType('audioop')
# ----------------------------

import nextcord
from nextcord.ext import commands
from datetime import datetime
import os

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")

@bot.event
async def on_member_join(member):
    channel_id = 1432474691381104707  # 👈 tu ID real del canal
    channel = bot.get_channel(channel_id)
    if channel:
        join_date = datetime.now().strftime("%B %d, %Y • %H:%M")
        embed = nextcord.Embed(
            title="👋 A new user has joined!",
            description=f"Hey {member.mention}, welcome to **Nuvix Market** 💫",
            color=nextcord.Color.from_rgb(130, 80, 255)
        )
        embed.add_field(name="👤 User", value=f"{member.mention}", inline=True)
        embed.add_field(name="📅 Joined On", value=join_date, inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="https://discord.com/channels/774256913646878752/1432475296522829844/1432708362465706056")
        embed.set_footer(text="Welcome System — Nuvix Market 💎")
        await channel.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Nuvix Market bot is alive.")

bot.run(os.getenv("TOKEN"))

# --- Mantener el bot activo en Render ---
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ NVIXXX bot is alive"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()
# --- Fin del keep alive ---
