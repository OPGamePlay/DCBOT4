import asyncio
from discord import app_commands
import discord
from urllib.parse import urlparse, parse_qs
import yt.ytdl as yt
import yt.Embed as ytE
import json
import random

queues = {}
import os


def load(bot: discord.client, tree: app_commands.CommandTree, guilds: list,
         config):

  @tree.command(name="youtube", description='Youtube Music', guilds=guilds)
  # @app_commands.describe(Input='Youtube Music')
  @app_commands.choices(methods=[
    app_commands.Choice(name='By Link', value=1),
    app_commands.Choice(name='By Search', value=2),
  ])
  async def youtube(interaction: discord.Interaction,
                    methods: app_commands.Choice[int], input: str):

    async def get_VoiceClient():
      VoiceChannel = interaction.user.voice.channel
      if interaction.guild.voice_client is None:
        VoiceClient = await VoiceChannel.connect()
      else:
        VoiceClient = interaction.guild.voice_client
      return VoiceClient

    if methods.value == 1:
      await interaction.response.send_message('載入中。。。', delete_after=3.0)
      YT_API = os.environ['YT_API']
      parse_url = urlparse(input)
      parse_url.hostname
      if parse_url.hostname == 'www.youtube.com' or parse_url.hostname == 'm.youtube.com' or parse_url.hostname == 'music.youtube.com':
        # if interaction.guild.id not in queues.keys():
        # queues[f"{interaction.guild.id}"] = []
        if os.path.isfile(f"yt/queues/{interaction.guild.id}.json") == False:
          q = []
          with open(f"yt/queues/{interaction.guild.id}.json", 'w') as f:
            json.dump(q, f)
        if (parse_url.path == '/playlist' and 'list=' in parse_url.query) or (
            'v=' in parse_url.query and 'list=' in parse_url.query):
          status, error, extracted_data = yt.ListData(
            parse_qs(parse_url.query), YT_API)
          if status == 'ok':

            # tmp_queue:list = queues[f"{interaction.guild.id}"]

            # tmp_queue: list = queues[f"{interaction.guild.id}"]
            # for video in extracted_data['videos']:
            #   tmp_queue.append(video)
            # queues[f"{interaction.guild.id}"] = tmp_queue

            # first_mes:discord.InteractionMessage = await interaction.original_response()
            # await first_mes.reply(queues)
            with open(f"yt/queues/{interaction.guild.id}.json", 'r') as file:
              tmp_queue = json.load(file)
              area_failed = 0
              for video in extracted_data['videos']:

                if 'HK' not in video['area']:
                  area_failed = area_failed + 1
                else:
                  tmp_queue.append(video)
            with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
              json.dump(tmp_queue, file)
            embed = ytE.create(extracted_data, 'playlist', tmp_queue)

            await interaction.channel.send(embed=embed, delete_after=3)

            VoiceClient: discord.VoiceClient = await get_VoiceClient()
            yt.play(VoiceClient, config)
            # while VoiceClient.is_connected() == False:
            #     pass

            # for video in extracted_data['videos']:

            # await interaction.response.send_message("List")
          elif status == 'failed':
            if error == 'playlistNotFound':
              await interaction.channel.send("Playlist NotFound: 播放清單可能不公開")
            else:
              await interaction.channel.send("Playlist NotFound")
          else:
            await interaction.channel.send("Unknown Error in YTList")

        elif parse_url.path == '/watch' and 'v=' in parse_url.query:
          status, error, extracted_data = yt.videoData(
            parse_qs(parse_url.query), YT_API)
          if status == 'ok':
            # tmp_queue: list = queues[f"{interaction.guild.id}"]
            # tmp_queue.append(extracted_data)
            # queues[f"{interaction.guild.id}"] = tmp_queue
            if 'HK' not in extracted_data['area']:
              await interaction.channel.send(
                embed=ytE.message('該地區無法下載該影片，已跳過'), delete_after=3),
            else:

              with open(f"yt/queues/{interaction.guild.id}.json", 'r') as file:
                tmp_queue = json.load(file)

              print(type(tmp_queue))
              tmp_queue.append(extracted_data)
              print(type(tmp_queue))

              with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
                json.dump(tmp_queue, file)

              embed = ytE.create(extracted_data, 'single', tmp_queue)
              await interaction.channel.send(embed=embed, delete_after=5)
              VoiceClient: discord.VoiceClient = await get_VoiceClient()
              yt.play(VoiceClient, config)

          elif status == 'failed':
            if error == 'playlistNotFound':
              await interaction.channel.send("Playlist NotFound: 播放清單可能不公開")
            else:
              await interaction.channel.send("Playlist NotFound")
          else:
            await interaction.channel.send("Unknown Error in YTList")

        elif parse_url.query == '' and '/shorts/' in parse_url.path:

          status, error, extracted_data = yt.shortData(parse_url.path, YT_API)
          if status == 'ok':
            # tmp_queue: list = queues[f"{interaction.guild.id}"]
            # tmp_queue.append(extracted_data)
            # queues[f"{interaction.guild.id}"] = tmp_queue
            if 'HK' not in extracted_data['area']:
              await interaction.channel.send(
                embed=ytE.message('該地區無法下載該影片，已跳過'), delete_after=3),
            else:

              with open(f"yt/queues/{interaction.guild.id}.json", 'r') as file:
                tmp_queue = json.load(file)

              tmp_queue.append(extracted_data)

              with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
                json.dump(tmp_queue, file)
              embed = ytE.create(extracted_data, 'short', tmp_queue)
              await interaction.channel.send(embed=embed, delete_after=3)
              try:
                VoiceClient: discord.VoiceClient = await get_VoiceClient()
              except Exception as err:
                print(err)
              yt.play(VoiceClient, config)

          elif status == 'failed':
            if error == 'playlistNotFound':
              await interaction.channel.send("Playlist NotFound: 播放清單可能不公開")
            else:
              await interaction.channel.send("Playlist NotFound")
          else:
            await interaction.channel.send("Unknown Error in YTList")

        else:
          await interaction.channel.send("Unsupported YT Link")
      else:
        await interaction.channel.send("Unsupported Link")
    # await interaction.response.send_message(f"r'{url}'")
    # ctx:discord.InteractionMessage = await interaction.original_response()
    # await ctx.reply(f"r'123566777'")

  @tree.command(name="skip", description='Youtube Music', guilds=guilds)
  # @app_commands.describe(Input='Youtube Music')
  async def skip(interaction: discord.Interaction):

    VoiceClient: discord.VoiceClient = interaction.guild.voice_client
    VoiceClient.stop()
    embed = ytE.message('影片已跳過')
    await interaction.response.send_message(embed=embed, delete_after=3)

  @tree.command(name="stop", description='Youtube Music', guilds=guilds)
  # @app_commands.describe(Input='Youtube Music')
  async def stop(interaction: discord.Interaction):

    VoiceClient: discord.VoiceClient = interaction.guild.voice_client
    VoiceClient.stop()
    VoiceClient.cleanup()
    await VoiceClient.disconnect()
    with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
      json.dump([], file)
    # queues[f"{interaction.guild.id}"].clear()

    embed = ytE.message('已停止播放並清空列隊')
    await interaction.response.send_message(embed=embed, delete_after=3)

  @tree.command(name="shuffle",
                description='Shuffle the Music queues',
                guilds=guilds)
  async def shuffle(interaction: discord.Interaction):
    with open(f"yt/queues/{interaction.guild.id}.json", 'r') as file:
      queues = json.load(file)
    random.shuffle(queues)
    with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
      queues = json.dump(queues, file)

  @bot.event
  async def on_interaction(interaction: discord.Interaction):
    if interaction.command != None:
      print(f"輸入: {interaction.command.name}\n 使用者: {interaction.user}")
    else:
      print('button pressed')
      if interaction.data['custom_id'] == 'shuffle':
        with open(f"yt/queues/{interaction.guild.id}.json", 'r') as file:
          queues = json.load(file)
        random.shuffle(queues)
        queues.append(queues[0])
        with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
          queues = json.dump(queues, file)
        embed = ytE.message('已隨機排列列隊')

        await interaction.response.send_message(embed=embed, delete_after=3)
        VoiceClient: discord.VoiceClient = interaction.guild.voice_client
        VoiceClient.stop()
      elif interaction.data['custom_id'] == 'skip':
        VoiceClient: discord.VoiceClient = interaction.guild.voice_client
        VoiceClient.stop()
        embed = ytE.message('影片已跳過')
        await interaction.response.send_message(embed=embed, delete_after=3)
      elif interaction.data['custom_id'] == 'stop':
        VoiceClient: discord.VoiceClient = interaction.guild.voice_client
        VoiceClient.stop()
        VoiceClient.cleanup()
        await VoiceClient.disconnect()
        with open(f"yt/queues/{interaction.guild.id}.json", 'w') as file:
          json.dump([], file)
        embed = ytE.message('已停止播放並清空列隊')
        await interaction.response.send_message(embed=embed)
