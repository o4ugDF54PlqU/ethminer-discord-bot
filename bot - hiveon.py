import discord
from discord.ext import tasks, commands
import asyncpg
import json
import requests
import imgkit
import GPUtil
from tabulate import tabulate
import numpy as np
import cv2
import pyautogui
import os

# insert your bot key here, get one from discord
key = 'key'

# channel to send updates and notifications to
notification_channel = 825054534044090408

# pool hash check, reboot if hash lower than desired_hash times_to_check times in a row
check_enabled = True
address = "696b18d7e003be5b4d1a66b981313e1959d69066"
desired_hash = 169000000
times_to_check = 3
worker_name = "WORKER001" # note: case sensitive

# do not change
low_hash = 0
startup = True

ping_data = {
  "id": 1,
  "jsonrpc": "2.0",
  "method": "miner_getstatdetail"
}

data_json = json.dumps(ping_data)
payload = {'json_payload': data_json}

class MyClient(discord.Client):

    async def on_ready(self):
        global low_hash
        low_hash = 0
        print('Logged on as', self.user)
        channel = client.get_channel(notification_channel)
        await channel.send(f'Reboot Detected!')

    async def on_message(self, message):
        # don't respond to ourselves
        #if message.author == self.user:
        #    return

        if message.content == 'reboot':
            print("REBOOTING")
            os.system("shutdown -t 0 -r")
            return

        if message.content == 'force reboot':
            print("REBOOTING")
            os.system("shutdown -t 0 -r -f")
            return

        if message.content == 'screenshot':
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
   
            # writing it to the disk using opencv
            cv2.imwrite("screen.png", image)
            await message.channel.send(file=discord.File('screen.png'))
            return
            

        if message.content == 'ping':
            r = requests.get('http://127.0.0.1:3333', data=payload)
            html_file = open("temp.html", "w")
            html_file.write(r.text)
            html_file.close()
            imgkit.from_file('temp.html', 'out.jpg')
            await message.channel.send(file=discord.File('out.jpg'))
            
            # Ethminer API doesn't report temperature for me for some reason
            # this is a backup method (only works for nvidia)
            await message.channel.send("="*40+"GPU Details"+"="*40)
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_id = gpu.id
                gpu_name = gpu.name
                gpu_load = f"{gpu.load*100}%"
                gpu_temperature = f"{gpu.temperature} ??C"
                list_gpus.append([
                    gpu_name, gpu_temperature, gpu_load])
            
            output = ("```" + "\n\n" + tabulate(list_gpus, tablefmt="plain", headers=["GPU", "Temps","Load"]) + "```")
            await message.channel.send(output)
            return

@tasks.loop(minutes = 10)
async def check_hashrate():
    global low_hash, startup
    channel = client.get_channel(notification_channel)
    try:
        await channel.send("ping")
        r = requests.get(f'https://hiveon.net/api/v1/stats/miner/{address}/ETH/workers')
        worker_data = r.json()["workers"][worker_name]
        
        if int(r.json()["reportedHashrate"]) < desired_hash:
            low_hash+=1
            current_hash = r.json()["reportedHashrate"]
            print(f"low hash detected: {current_hash}, {low_hash} times")
            if low_hash >= times_to_check:
                await channel.send(f"@everyone hash too low: {current_hash}, rebooting")
                await channel.send("screenshot")
                os.system("shutdown -t 10 -r")
                return
            else:
                await channel.send(f"low hash warning: {current_hash}")
        else:
            low_hash = 0

        startup = False
        
    except requests.ConnectionError:
        print("error, no internet")
    except KeyError:
        if startup:
            startup = False
            print("not in pool during startup")
        else:
            print("not in pool")
            await channel.send("worker not found on pool, rebooting")
            await channel.send("screenshot")
            os.system("shutdown -t 10 -r")
    except AttributeError:
        print("not logged on yet")

if check_enabled:
    check_hashrate.add_exception_type(asyncpg.PostgresConnectionError)
    check_hashrate.start()

client = MyClient()
client.run(key)
