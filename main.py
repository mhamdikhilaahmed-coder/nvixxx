import nextcord
from nextcord.ext import commands
from nextcord import Embed
import os
from flask import Flask
from threading import Thread

# === BOT CONFIG ===
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True  # Needed for join/leave events

bot = commands.Bot(command_prefix="!", intents=intents)

# === EVENT: Bot Ready ===
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# === EVENT: Welcome Message ===
@bot.event
async def on_member_join(member):
    # 👇 Replace this with your actual welcome channel ID
    WELCOME_CHANNEL_ID = 1432474691381104707  

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = Embed(
            title="🎉 Welcome to Nuvix Market!",
            description=f"Hey {member.mention}, we're glad to have you here! 💫\n\nExplore the channels and enjoy your stay!",
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Nuvix Market — Your wishes, more cheap!")
        await channel.send(embed=embed)
        print(f"🟢 Welcomed {member.name}")
    else:
        print("⚠️ Couldn't find the welcome channel.")

# === EVENT: Goodbye Message ===
@bot.event
async def on_member_remove(member):
    # 👇 Optional: Replace this with your goodbye channel ID
    GOODBYE_CHANNEL_ID = 123456789012345678  

    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        embed = Embed(
            title="👋 Goodbye!",
            description=f"{member.name} has left the server. We hope to see you again soon!",
            color=0xFF5555
        )
        embed.set_footer(text="Nuvix Market — We'll miss you 💔")
        await channel.send(embed=embed)
        print(f"🔴 {member.name} left the server.")

# === COMMANDS ===
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! The bot is active and running.")

@bot.command()
async def info(ctx):
    embed = Embed(
        title="📘 Server Info",
        description="Welcome to **Nuvix Market** — The best place for your digital wishes!",
        color=0x00FFB0
    )
    embed.add_field(name="👑 Owner", value="YourNameHere", inline=True)
    embed.add_field(name="🌐 Website", value="[Visit Here](https://nviXXX.onrender.com/)", inline=True)
    embed.set_footer(text="Nuvix Market — Powered by Nextcord")
    await ctx.send(embed=embed)

# === FLASK KEEP-ALIVE SERVER (for Render) ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Nuvix Market Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === RUN BOT ===
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")  # Store your token securely in Render
    bot.run(TOKEN)
