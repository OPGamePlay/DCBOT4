import asyncio
import json
import shutil
import time
import yt_dlp
import requests
import discord
import os
import yt.Embed as ytE
import random
from yt_dlp.utils import DownloadError


def ListData(link_parameter, api):
  item_per_page = 50
  status = 'none'
  error = 'none'
  extracted_data = {}
  respones = requests.get(
    f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId={link_parameter['list'][0]}&key={api}&maxResults={item_per_page}"
  )
  data: dict = respones.json()
  if respones.status_code == 404:
    status = 'failed'
    if data['error']['errors'][0]['reason'] == 'playlistNotFound':
      error = 'notfound'
  elif respones.status_code == 200:
    next = True
    items = []
    PageToken = ''
    unaviabled = 0
    page = 0
    while (next == True):
      if page > 3:
        next = False
        break
      if items != []:
        respones = requests.get(
          f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId={link_parameter['list'][0]}&key={api}&maxResults={item_per_page}&pageToken={PageToken}"
        )
        data: dict = respones.json()
      if 'nextPageToken' in data.keys():
        PageToken = data['nextPageToken']
        next = True
      else:
        next = False
      print(respones.status_code)
      status = 'ok'
      
      

      for video in data['items']:
        contentDetails = data['items'][0]['contentDetails']
        contentDetails.keys()
        if 'regionRestriction' in contentDetails.keys():
          area = video['contentDetails']['regionRestriction'][
            'allowed']
        else:
          area = ['HK']
        
        if video['snippet']['title'] == 'Deleted video' or video['snippet'][
            'title'] == 'Private video':
          unaviabled = unaviabled + 1
          continue
        item = {
          "title": video['snippet']['title'],
          "thumbnails": video['snippet']['thumbnails']['default']['url'],
          "vid": video['snippet']['resourceId']['videoId'],
          "url":
          f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}",
          "area": area
        }
        items.append(item)
      page = page + 1
    extracted_data = {
      "count": data['pageInfo']['totalResults'],
      "videos": items,
      "unaviabled": unaviabled
    }

  else:
    status = 'failed'
    error = 'unknown'
  # print(respones.json())

  return status, error, extracted_data


def shortData(link_parameter, api):
  status = 'none'
  error = 'none'
  extracted_data = {}
  respones = requests.get(
    f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status&id={link_parameter[8:]}&key={api}"
  )
  data: dict = respones.json()

  if respones.status_code == 404:
    status = 'failed'
    if data['error']['errors'][0]['reason'] == 'playlistNotFound':
      error = 'notfound'
  elif respones.status_code == 200:
    status = 'ok'
    contentDetails: dict = data['items'][0]['contentDetails']
    if 'regionRestriction' in contentDetails.keys():
      area = data['items'][0]['contentDetails']['regionRestriction']['allowed']
    else:
      area = ['HK']
    extracted_data = {
      "title": data['items'][0]['snippet']['title'],
      "thumbnails":
      data['items'][0]['snippet']['thumbnails']['default']['url'],
      "vid": data['items'][0]['id'],
      "url": f"https://www.youtube.com/watch?v={data['items'][0]['id']}",
      "area": area
    }
  return status, error, extracted_data


def videoData(link_parameter, api):
  status = 'none'
  error = 'none'
  extracted_data = {}
  respones = requests.get(
    f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status&id={link_parameter['v'][0]}&key={api}"
  )
  data: dict = respones.json()

  if respones.status_code == 404:
    status = 'failed'
    if data['error']['errors'][0]['reason'] == 'playlistNotFound':
      error = 'notfound'
  elif respones.status_code == 200:
    status = 'ok'
    contentDetails: dict = data['items'][0]['contentDetails']
    if 'regionRestriction' in contentDetails.keys():
      area = data['items'][0]['contentDetails']['regionRestriction']['allowed']
      print(area)
    else:
      area = ['HK']
    extracted_data = {
      "title": data['items'][0]['snippet']['title'],
      "thumbnails": data['items'][0]['snippet']['thumbnails']['medium']['url'],
      "vid": data['items'][0]['id'],
      "url": f"https://www.youtube.com/watch?v={data['items'][0]['id']}",
      "area": area
    }

  return status, error, extracted_data


def play( VoiceClient: discord.VoiceClient, config , mes = None):

  button_shuffle = discord.ui.Button(
    label="隨機清單", custom_id='shuffle',style= discord.ButtonStyle.primary
                             )
  button_skip = discord.ui.Button(
    label="跳過", custom_id='skip',style= discord.ButtonStyle.primary
                             )
  button_refresh = discord.ui.Button(
    label="停止", custom_id='stop',style= discord.ButtonStyle.primary
                             )
  class gui(discord.ui.View):
    def __init__(self):
      super().__init__()
      self.add_item(button_shuffle)
      self.add_item(button_skip)
      self.add_item(button_refresh)

  with open(f"yt/queues/{VoiceClient.guild.id}.json", 'r') as file:
    queues = json.load(file)
  # print(queues)
  if VoiceClient.is_playing() is False:
    with open(f"dat/setting/{VoiceClient.guild.id}.json", 'r') as file:
      j = json.load(file)

      def after(err: Exception):
        
        print(err)
        if err == None:
          source.cleanup()
          with open(f"yt/queues/{VoiceClient.guild.id}.json", 'r') as file:
            queues = json.load(file)
          os.remove(
            f"yt/temp/{VoiceClient.guild.id}/{VoiceClient.guild.id}.wav")
          if len(queues) <= 1:
            VoiceClient.stop()
            asyncio.run_coroutine_threadsafe(VoiceClient.disconnect(),
                                             VoiceClient.client.loop)
                                             
            asyncio.run_coroutine_threadsafe(
              channel.send(embed=ytE.message("播放結束")), VoiceClient.client.loop)
            VoiceClient.cleanup()
            with open(f"yt/queues/{VoiceClient.guild.id}.json", 'w') as file:
              json.dump([], file)
            asyncio.run_coroutine_threadsafe(mes.result().delete(), VoiceClient.client.loop)
            return
          else:
            queues.pop(0)
            with open(f"yt/queues/{VoiceClient.guild.id}.json", 'w') as file:
              json.dump(queues, file)
            time.sleep(2)
            return play(VoiceClient, config , mes = mes)

        elif err == TimeoutError:
          try:
            folder = f"yt/temp/{VoiceClient.guild.id}"
            for filename in os.listdir(folder):
              file_path = os.path.join(folder, filename)
              try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                  os.unlink(file_path)
                elif os.path.isdir(file_path):
                  shutil.rmtree(file_path)
              except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            print(err)
          except Exception as err2:
            print(err)
            print(err2)
        elif err == 'unavailable':
          with open(f"yt/queues/{VoiceClient.guild.id}.json", 'r') as file:
            queues = json.load(file)
          if len(queues) <= 1:
            VoiceClient.stop()
            asyncio.run_coroutine_threadsafe(VoiceClient.disconnect(),
                                             VoiceClient.client.loop)
            asyncio.run_coroutine_threadsafe(
              channel.send(embed=ytE.message("播放結束")), VoiceClient.client.loop)
            VoiceClient.cleanup()
            with open(f"yt/queues/{VoiceClient.guild.id}.json", 'w') as file:
              json.dump([], file)
            asyncio.run_coroutine_threadsafe(mes.result().delete(), VoiceClient.client.loop)
            return
          else:
            queues.pop(0)
            with open(f"yt/queues/{VoiceClient.guild.id}.json", 'w') as file:
              json.dump(queues, file)
            time.sleep(2)
            return play(VoiceClient, config , mes = mes)
        else:
          print('unknown error : ' + err)


      err = False
      class loggerOutputs:
        def error(msg):
          print("Captured Error: "+msg)
          return True

        def warning(msg):
          print("Captured Warning: "+msg)
        def debug(msg):
          print("Captured Log: "+msg)
      
      

      ydl_opts = {
        'outtmpl':
        f"yt/temp/{VoiceClient.guild.id}/{VoiceClient.guild.id}.wav",
        'format': 'bestaudio',
        'skip': ['hls', 'dash', 'translated_subs'],
        'player_skip': ['configs'],
        'ignoreerrors' : 'only_download',
        "logger": loggerOutputs,
        "quiet": True,
      }
      print('play')
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        channel = VoiceClient.client.get_channel(int(j['music_channel']))
        with open(f"yt/queues/{VoiceClient.guild.id}.json", 'r') as file:
          queues = json.load(file)
          with open(f"yt/queues/{VoiceClient.guild.id}.json", 'w') as file:
              json.dump(queues, file)
          try:
            ydl.extract_info(queues[0]['vid'], download=True)
          except DownloadError:
              print("An exception has been caught")
          
          # print(info)




            
          
          
          if os.path.isfile(f"yt/temp/{VoiceClient.guild.id}/{VoiceClient.guild.id}.wav") == False :
            after('unavailable')

          else:
            if mes == None:
              button = gui()
              mes = asyncio.run_coroutine_threadsafe(
                  channel.send(
                    embed=ytE.create(data=None, type='current', queues=queues),view=button),
                  VoiceClient.client.loop)
              print("sent")
            else:
              mes = asyncio.run_coroutine_threadsafe(
                  mes.result().edit(
                    embed=ytE.create(data=None, type='current', queues=queues)),
                  VoiceClient.client.loop)
            source = discord.FFmpegOpusAudio(
              source=f"yt/temp/{VoiceClient.guild.id}/{VoiceClient.guild.id}.wav")
            try:
              VoiceClient.play(source, after=after)
            except Exception as err:
              print(err)
              asyncio.run_coroutine_threadsafe(
                channel.send(f"Unknown Error: {err}", VoiceClient.client.loop))




if __name__ == '__main__':
  pass
