from discord import embeds


def create(data,type,queues):
    if type == 'playlist':
        embed = embeds.Embed(title=f"列隊中共有{len(queues)}條片",color=13762560)
        embed.set_author(name=f"此爲播放清單|内含{data['count']}條片|{data['unaviabled']}為私人或已移除影片")



    if type == 'single':
        embed = embeds.Embed(title=f"列隊中共有{len(queues)}條片",color=13762560)
        embed.set_author(name="此爲影片")
    if type == 'short':
        embed = embeds.Embed(title=f"列隊中共有{len(queues)}條片",color=13762560)
        embed.set_author(name="此爲Short")
    if type == 'current':
        embed = embeds.Embed(title=f"正在播放{queues[0]['title']}",color=13762560,description=f"列隊中共有{len(queues)}條片")
        embed.set_author(name="Music")
        embed.set_image(url=queues[0]['thumbnails'])
        value = ''
        for index,vname in enumerate(queues):
            if index == 0:
                continue
            elif index == 1:
                value = value + str(index) + '. ' + vname['title'] + '\n'
            elif index < 11:
                value = value + str(index) + '. ' + vname['title'] + '\n'
            else :
              break
            
        embed.add_field(name='列隊預覽(最大為10): ',value=value,inline=False)
    embed.set_thumbnail(url="https://www.youtube.com/s/desktop/b182fc95/img/favicon_96x96.png")
    return embed

def message(mess):
    embed = embeds.Embed(title=mess,color=13762560)
    embed.set_author(name=f"通知")
    embed.set_thumbnail(url="https://www.youtube.com/s/desktop/b182fc95/img/favicon_96x96.png")
    return embed