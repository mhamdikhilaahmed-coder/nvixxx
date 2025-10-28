import os
import nextcord
from nextcord.ext import commands
from flask import Flask
from threading import Thread

# --- Discord Bot Setup ---
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_member_join(member):
    channel_id = 1432474691381104707  # replace with your welcome channel ID
    channel = bot.get_channel(channel_id)

    if channel:
        embed = nextcord.Embed(
            title="🎉 Welcome to Nuvix Market!",
            description=(
                f"Hey {member.mention}! 👋\n\n"
                "Welcome to **Nuvix Market** — the best place for your deals and wishes!\n"
                "Make sure to check out <#1432474691381104708> for rules and <#1432474691381104709> to verify your account."
            ),
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text="Nuvix Market — Your wishes, more cheap!")
        await channel.send(embed=embed)

    try:
        await member.send(
            f"👋 Hi {member.name}! Welcome to **Nuvix Market**.\n"
            "Enjoy your stay and check our rules and store sections!"
        )
    except:
        pass


# --- Flask Keepalive Server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Nuvix Market Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# --- Run both Flask and Discord bot ---
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
