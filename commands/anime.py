import os
from discord import app_commands
import discord
import requests
import datetime
import json
import time

domain = 'https://api.jikan.moe/v4/'


def get_seasons_list(year: int, season: str):
  path = f"seasons/{year}/{season}/"
  r = requests.get(domain + path)

  js = r.json()
  # print(js)

  datas = []
  for data in js['data']:
    datas.append(data)
  time.sleep(1)
  page = 2
  while True:
    r = requests.get(f"{domain}{path}/?page={page}")
    js = r.json()
    for data in js['data']:
      datas.append(data)
    page = page + 1

    if js['pagination']['has_next_page'] == True:
      time.sleep(1)
      continue
    else:
      break

  animes = []
  for anime in datas:
    studios = []
    for studio in anime['studios']:
      studios.append(studio['name'])
    animes.append({
      "title": anime['title_japanese'],
      "title_eng": anime['title'],
      "air_time": {
        "year": anime['aired']['prop']['from']['year'],
        "month": anime['aired']['prop']['from']['month'],
        "day": anime['aired']['prop']['from']['day'],
        "weekday": anime['broadcast']['day'],
        "time": anime['broadcast']['time'],
      },
      "image": anime['images']['jpg']['image_url'],
      "studios": studios,
    })
  dat = {}
  dat['animes'] = animes
  return dat


def check_Data(year: int, season: str):
  return os.path.isdir(f"./anime/{year}/{season}")


def get_season():
  month = datetime.datetime.now().month
  s = int((month + 2) / 3)
  if s == 2:
    return 'spring'
  if s == 3:
    return 'summer'
  if s == 4:
    return 'fall'  # autumn
  if s == 1:
    return 'winter'


def load(tree: app_commands.CommandTree, guilds: list):

  @tree.command(name='anilist', description='Show Anime List', guilds=guilds)
  async def anilist(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    season = get_season()
    year = datetime.datetime.now().year
    if check_Data(year, season) == False:
      os.makedirs(f"./anime/{year}/{season}/")
      js: json = get_seasons_list(year, season)
      with open(f"./anime/{year}/{season}/data.json", 'w') as file:
        date = {
            'year': datetime.datetime.now().year,
            'month': datetime.datetime.now().month,
            'day': datetime.datetime.now().day
        }
        js['lastupdate'] = date
        json.dump(js, file, indent=4)

    with open(f"./anime/{year}/{season}/data.json", 'r') as file:
      dat = json.load(file)
      embeds = []
      js = dat['animes']
      anime_weekdays = []
      anime_weekdays.append(
        (anime for anime in js if anime['air_time']['weekday'] == 'Sundays'))
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Mondays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Tuesdays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Wednesdays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Thursdays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Fridays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == 'Saturdays')
      anime_weekdays.append(anime for anime in js
                            if anime['air_time']['weekday'] == None)
      x = 0
      for anime_weekday in anime_weekdays:
        for anime in anime_weekday:

          embed = discord.Embed(
            title=anime['title'],
            description=f"{anime['title_eng']}\n"
            f"製作組為{anime['studios']}\n"
            f"首播於{anime['air_time']['year']}年{anime['air_time']['month']}月{anime['air_time']['day']}日\n"
            f"播放於{anime['air_time']['weekday']}| 日本時間{anime['air_time']['time']}",
            color=16711935)
          embed.set_image(url=anime['image'])
          embeds.append(embed)
          x = x + 1
          if x == 10:
            await interaction.followup.send(embeds=embeds, ephemeral=True)
            x = 0
            embeds.clear()

      if x > 0:
        await interaction.followup.send(embeds=embeds, ephemeral=True)
        embeds.clear()
      embed = discord.Embed(color=16711935,title="動漫列表",description=f"最後更新時間為{dat['lastupdate']['year']}年{dat['lastupdate']['month']}月{dat['lastupdate']['day']}日\n使用/aniupdate 更新最新資訊")

      await interaction.followup.send(embed=embed, ephemeral=True)

  @tree.command(name='aniupdate',
                description='Update Anime List',
                guilds=guilds)
  async def aniupdate(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    season = get_season()
    year = datetime.datetime.now().year
    try:
      os.makedirs(f"./anime/{year}/{season}/")
    except:
      pass
    js: json = get_seasons_list(year, season)
    with open(f"./anime/{year}/{season}/data.json", 'w') as file:
      date = {
        'year': datetime.datetime.now().year,
        'month': datetime.datetime.now().month,
        'day': datetime.datetime.now().day
      }
      js['lastupdate'] = date
      json.dump(js, file, indent=4)
    embed = discord.Embed(color=16711935,title="列表更新完成",description=f"最後更新時間為{js['lastupdate']['year']}年{js['lastupdate']['month']}月{js['lastupdate']['day']}日")
    await interaction.followup.send(embed=embed, ephemeral=True)
