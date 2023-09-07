import datetime
from discord import app_commands 
import discord 
import json
import os
import shutil

def load(bot:discord.client):
    

        

    @bot.event
    async def on_voice_state_update(member:discord.Member, before, after):
        guild_id = member.guild.id
        with open(f"dat/setting/{guild_id}.json") as file:
            config = json.load(file)
        if config['member_change'] == True:
            channel = config['member_change_channel']
            #change
            if before.channel != after.channel:
                #join
                embed = discord.Embed()
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name=f'{member}', icon_url=f'{member.avatar.url}')
                dchannel  = bot.get_channel(int(channel))
                if before.channel == None and after.channel != None:
                    embed.description = f'{member.mention} 插咗入 <{after.channel.name}> 度'
                    embed.colour = 0x1ec81e
                    await dchannel.send(embed=embed)
                    print("join %s" % after.channel.name)
                #leave
                if before.channel != None and after.channel == None:
                    if member.id == 505965675186225162:
                      folder = f"yt/temp/{member.guild.id}"
                      for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        try:
                          if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                          elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                        except Exception as e:
                          print('Failed to delete %s. Reason: %s' % (file_path, e))
                    embed.description = f'{member.mention} 喺 <{before.channel.name}> 抽返出嚟'
                    embed.colour = 0xc81e1e
                    await dchannel.send(embed=embed)
                    print("left %s" % before.channel.name)
                #move
                if before.channel != None and after.channel != None:
                    if (
                    before.afk == after.afk and
                    before.deaf == after.deaf and
                    before.mute == after.mute and
                    before.requested_to_speak_at == after.requested_to_speak_at and
                    before.self_deaf == after.self_deaf and
                    before.self_mute == after.self_mute and
                    before.self_stream == after.self_stream and
                    before.self_video == after.self_video and
                    before.suppress == after.suppress
                    ):
                        embed.description = f'{member.mention} 由 <{before.channel.name}> 走咗去 <{after.channel.name}>'
                        embed.colour = 0x1e1ec8
                        await dchannel.send(embed=embed)
                        print("%s move to  %s" % (before.channel.name ,after.channel.name))