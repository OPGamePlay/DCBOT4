import commands.play
import commands.member_change
import commands.anime
from discord import Object



def load(bot,tree,config):
    guilds_ob = []
    for id in config['guild']:
        guilds_ob.append(Object(id=id))
    commands.play.load(bot,tree,guilds_ob,config)
    commands.anime.load(tree,guilds_ob,)
    commands.member_change.load(bot)