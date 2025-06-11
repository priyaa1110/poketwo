import discord
from discord.ext import commands
import datetime
import json
import os

PLAYER_DATA_PATH = "data/players.json"
QUEST_LIST = [
    {"type": "catch", "count": 3, "description": "Catch 3 different Pokémon"},
]

def load_data():
    if os.path.exists(PLAYER_DATA_PATH):
        with open(PLAYER_DATA_PATH, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(PLAYER_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def assign_daily_quest(self, user_id, data):
        from random import choice
        quest = choice(QUEST_LIST)
        data[str(user_id)]["quest"] = {
            "type": quest["type"],
            "count": quest["count"],
            "progress": 0,
            "description": quest["description"],
            "assigned": str(datetime.date.today())
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        data = load_data()
        if str(user_id) not in data:
            data[str(user_id)] = {}
        user_data = data[str(user_id)]
        today = str(datetime.date.today())

        if "quest" not in user_data or user_data["quest"].get("assigned") != today:
            self.assign_daily_quest(user_id, data)
            save_data(data)

    @commands.command(name="quest")
    async def quest(self, ctx):
        user_id = str(ctx.author.id)
        data = load_data()
        if user_id not in data or "quest" not in data[user_id]:
            await ctx.send("No active quest found.")
            return
        quest = data[user_id]["quest"]
        await ctx.send(f"📜 **Today's Quest:** {quest['description']}\nProgress: {quest['progress']}/{quest['count']}")

def setup(bot):
    bot.add_cog(Quests(bot))
  
