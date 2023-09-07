import asyncio
import sys
import discord
from discord.ext import commands
import threading
from discord import app_commands 
import gradio as gr
import os

# intents = discord.Intents.default()
# intents.message_content = True

# bot = commands.Bot(command_prefix='-',intents=intents)

# def sd(shutdown_wait):
#     shutdown_wait.clear()
#     shutdown_wait.wait()
#     print("shuting down")
#     bot.close()

def start(status:threading.Event,shutdown_wait:threading.Event,bot:discord.Client,tree:app_commands.CommandTree,config,Dropdown:gr.Dropdown):


    # @bot.command()
    # async def syncCommand(tree):
    #     await app_commands.CommandTree.sync(guild=discord.Object(id=449816847831924738))
    #     print('Command synced')


    

    @bot.event
    async def on_connect():
        for id in config['guild']:
            await tree.sync(guild=discord.Object(id=id))
        



        print('Command synced')

        print("Hello World")
        




        
        status.set()
        
        await asyncio.sleep(5)

        # shutdown = threading.Thread(target = sd, args= (shutdown_wait,))
        # await shutdown.run()
        
    @bot.event
    async def on_disconnect():
        print('bye world')
        

    @bot.event
    async def on_error(event,*args, **kwargs):
        await asyncio.sleep(3)
        print(f"event: {event}\nargs: {args}\nkwargs: {kwargs}")


    # @bot.event
    # async def on_interaction(interaction:discord.Interaction):
    #     await asyncio.sleep(3)
    #     if interaction.command != None:
    #         print(f"輸入: {interaction.command.name}\n 使用者: {interaction.user}")
    #     else:
    #         print('button pressed')
        



    # @bot.event
    # async def on_error(self, ctx, error):
    #     await ctx.reply(error, ephemeral = True)
    # @tree.command()
    # async def down(self):
    #     # threading.currentThread
    #     try:
    #         await bot.close()

    #     except Exception as err:
    #         print(err)


    # if before == False:



    asyncio.run(bot.start(os.getenv("TOKEN"),reconnect=True))


