from discord import app_commands 
import discord 

def load(tree:app_commands.CommandTree):
    @tree.command(name='',description='',guild = discord.Object(id=449816847831924738))
    async def play(interaction:discord.Interaction, text:str):
        pass