import shutil
import gradio as gr
import Discord_loop
import threading
import discord
from discord.ext import commands
from discord import app_commands 
import asyncio
import cus_commands
import json
import os 
import alive

global before,bot,console

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True


status = threading.Event()
shutdown_wait = threading.Event()

bot = discord.Client(command_prefix='-',intents=intents)


def init_config():
    folder = "./yt/temp/"
    if len(os.listdir(folder)) != 0:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    folder = "./yt/queues/"
    if len(os.listdir(folder)) != 0:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    with open('config.json','r') as file:
        data = json.load(file)
        return data

def tl_list(lis):
    text = ""
    for item in lis:
          text = f"{item}\n{text}"
    return text
def start():
    try:
        if status.is_set() == False:
            global client,bot, tree, config, gui, Dropdown
            
            tree = app_commands.CommandTree(bot)

            cus_commands.load(bot,tree,config)

            client = threading.Thread(target = Discord_loop.start, args= (status,shutdown_wait,bot,tree,config,Dropdown))
            client.start()
            
            print('locked and wait')
            status.wait()

            print('ok')

            


            return "Done!" , tl_list(threading.enumerate())
        else:
            return "Error : Discord Bot已經為開啓狀態!" , tl_list(threading.enumerate())
    except Exception as err:
        print(err)
        return "Error: 無法啓動Discord Bot" , tl_list(threading.enumerate())

def shutdown():
    if status.is_set() == False:
        return "Error: Discord Bot已經為關閉狀態" , tl_list(threading.enumerate())
    else:
        try:
            global before, client, tree, bot
            before = True
            status.clear()
            
            # f = tree.get_command("down")
            try:
                asyncio.run(bot.close())
            except Exception as  err:
                print("Shutting Down... [%s]" % err)

            # time.sleep(2)
            # bot.clear()
            # print(tree.all_commands.clear())
            # print(bot.all_commands)

            bot = discord.Client(command_prefix='-',intents=intents)
            while client.is_alive() is True:
                pass
            return "Shutdowned!" , tl_list(threading.enumerate())
        except Exception as err:
                print(err)
                return "Error: 無法終止Discord Bot" , tl_list(threading.enumerate())

def initConfig():
    choice = []
    dir_list = os.listdir('dat/setting')
    name_list = []
    for dir in dir_list:
        name_list.append(dir[:-5])
    for guild in bot.guilds:
        if str(guild.id) not in name_list:
            with open(f"dat/setting/{str(guild.id)}.json",'w') as file:
                data = {
                    'name': guild.name,
                    'id' : guild.id,
                    'member_change' : False,
                    'member_change_channel' : 'None',
                    'music': False,
                    'music_channel': 'None'
                }
                json.dump(data, file, indent=4)
        choice.append(f"{guild.name}({guild.id})")

    # with open('dat/setting/guild_name.json','r+') as file:
    #     with open('dat/setting/member_change_switch.json','r+') as file2:
    #         member_change_switch_j = json.load(file2)
    #         config_j = json.load(file)

    #         for guild in bot.guilds:
    #             if str(guild.id) not in member_change_switch_j:
    #                 member_change_switch_j[guild.id] = False
    #             config_j[str(guild.id)] =  guild.name
    #             choice.append(guild.name)
    #         file.seek(0)
    #         file2.seek(0)
    #         json.dump(member_change_switch_j, file2)
    #         json.dump(config_j, file)
    #         file.truncate()
    #         file2.truncate()

    return gr.update(
        choices=choice,interactive=True
    )


def changeConfig(Dropdown):

    if Dropdown == 'None':
        return (
            gr.update(value=False,interactive=True,visible = False),
            gr.update(value=False,interactive=True,visible = False),
            gr.update(value=False,interactive=True,visible = False),
            gr.update(value=False,interactive=True,visible = False),
            )
    else:
        id = Dropdown[Dropdown.find("(")+1:Dropdown.find(")")]

        with open(f"dat/setting/{id}.json",'r') as file:
            j = json.load(file)
            member_change_select = j['member_change']
            music_select = j['music']
#==================
            guild = bot.get_guild(int(id))
            member_change_channel_list_with_ID_name = []
            for channel in guild.channels:
                member_change_channel_list_with_ID_name.append(f"{channel.name}({channel.id})")
            
            member_change_channel_No = j['member_change_channel']
            if member_change_channel_No == 'None' :
                show_guild_with_ID_name = 'None'
            else:
                show_guild = bot.get_channel(int(member_change_channel_No))
                show_guild_with_ID_name= f"{show_guild.name}({show_guild.id})"
#==================
            music_channel_list_with_ID_name = []
            for channel in guild.channels:
                music_channel_list_with_ID_name.append(f"{channel.name}({channel.id})")

            music_channel_No = j['music_channel']
            if music_channel_No == 'None' :
                show_guild_with_ID_name_m = 'None'
            else:
                show_guild_m = bot.get_channel(int(music_channel_No))
                show_guild_with_ID_name_m= f"{show_guild_m.name}({show_guild_m.id})"
            return (
                gr.update(value=member_change_select,interactive=True,visible = True),

                gr.update(choices = member_change_channel_list_with_ID_name,value=show_guild_with_ID_name,interactive=True,visible = True),
                
                gr.update(value=music_select,interactive=True,visible = True),

                gr.update(choices = music_channel_list_with_ID_name,value=show_guild_with_ID_name_m,interactive=True,visible = True),
            )
    
def submit(choice,member_change,member_change_channel,music,music_channel):
    try:
        id = choice[choice.find("(")+1:choice.find(")")]
        member_change_channel_id = member_change_channel[member_change_channel.find("(")+1:member_change_channel.find(")")]
        music_channel_id = music_channel[music_channel.find("(")+1:music_channel.find(")")]

        with open(f"dat/setting/{id}.json",'r+') as file:
            config_j = json.load(file)
            config_j['member_change'] = member_change
            config_j['member_change_channel'] = member_change_channel_id
            config_j['music'] =  music
            config_j['music_channel'] = music_channel_id


            file.seek(0)
            json.dump(config_j, file,indent=4)
            file.truncate()
        return "Submited Sucssefully"
    except Exception as err:
        return "Error : %s" % err

with gr.Blocks() as gui:
    
    gr.Markdown("HermanYeung v3.0")

    with gr.Tabs(selected=0):
        with gr.TabItem('log',id=1):
            tl = gr.Textbox(label = "Threads List",lines=7)
        with gr.TabItem('config',visible=False,id=2) as conifg_tb:
                Dropdown = gr.Dropdown(
                ['None'], label="已加入的伺服器", info="Guilds" 
                )
                with gr.Row():
                    member_change_switch = gr.Checkbox(value=False,visible=False,label='抽插記錄')
                    member_change_channel_dd = gr.Dropdown(['None'], label="頻道",visible=False)
                with gr.Row():
                    Music_switch = gr.Checkbox(value=False,visible=False,label='Youtube Music')
                    Music_log_channel_dd = gr.Dropdown(['None'], label="頻道",visible=False)

                Dropdown.change(fn=changeConfig,inputs=Dropdown,outputs=[
                    #update components
                    member_change_switch,
                    member_change_channel_dd,
                    Music_switch,
                    Music_log_channel_dd


                ])
                with gr.Row():
                    submit_log = gr.Textbox(value='None',label='Submit status')
                    submit_btn = gr.Button('Submit', variant="primary")
                    submit_btn.click(fn=submit,inputs = [Dropdown,member_change_switch,member_change_channel_dd,Music_switch,Music_log_channel_dd], outputs = submit_log)
        with gr.TabItem("control",id=0): 
            log = gr.Textbox(label="Output Box")

            start_btn = gr.Button("Bot Start",variant="primary")
            
            shutdown_btn = gr.Button("Shutdown")
            start_btn.click(fn=start, outputs=[log, tl])
            start_btn.style(size=['sm'])
            
            
            shutdown_btn.click(fn=shutdown, outputs=[log, tl])

            
            p_url = gr.Textbox(label="Url input Box")
            p_channel = gr.Textbox(label="Url input Box")
            p_btn = gr.Button("Play",variant="primary")


            log.change(fn=initConfig,outputs=Dropdown)
            # p_btn.click(fn=play,inputs=[p_url,p_channel])

def launch(input):
    print('starting...')
    
    before = False
    global config , console
    console = input
    config = init_config()
    config['guild']
    start()
    gui.launch(server_name='0.0.0.0')   
    