import discord
from discord.ext import tasks, commands
import asyncpg
import json
import requests
import imgkit
# GPU information
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
address = "696b18d7e003be5b4d1a66b981313e1959d69066"
desired_hash = 191000000
low_hash = 0
times_to_check = 3

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
        await channel.send('Reboot Detected!')

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
            await message.channel.send("="*40+"GPU Details"+"="*40)
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                # get the GPU id
                gpu_id = gpu.id
                # name of GPU
                gpu_name = gpu.name
                # get % percentage of GPU usage of that GPU
                gpu_load = f"{gpu.load*100}%"
                # get GPU temperature in Celsius
                gpu_temperature = f"{gpu.temperature} °C"
                list_gpus.append([
                    gpu_name, gpu_temperature, gpu_load])
            
            output = ("```" + "\n\n" + tabulate(list_gpus, tablefmt="plain", headers=["GPU", "Temps","Load"]) + "```")
            await message.channel.send(output)
            return

# Comment out this part if you don't want to check with pool
@tasks.loop(minutes = 5)
async def check_hashrate():
    global low_hash
    channel = client.get_channel(notification_channel)
    try:
        r = requests.get(f'https://hiveon.net/api/v1/stats/miner/{address}/ETH')
                
        if int(r.json()["reportedHashrate"]) < desired_hash:
            low_hash+=1
            current_hash = r.json()["reportedHashrate"]
            print(f"low hash detected: {current_hash}, {low_hash} times")
            if low_hash >= times_to_check:
                await channel.send(f"hash too low: {current_hash}")
                await channel.send("screenshot")
                await channel.send("ping")
                os.system("shutdown -t 10 -r")
                return
        else:
            low_hash = 0

    
    except requests.ConnectionError:
        print("error, no internet")

check_hashrate.add_exception_type(asyncpg.PostgresConnectionError)
check_hashrate.start()
# stop commenting here if you don't want to check with pool

client = MyClient()
client.run(key)