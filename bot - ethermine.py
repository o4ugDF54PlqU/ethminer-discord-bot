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

ping_data = {
  "id": 1,
  "jsonrpc": "2.0",
  "method": "miner_getstatdetail"
}

data_json = json.dumps(ping_data)
payload = {'json_payload': data_json}
address = "696b18d7e003be5b4d1a66b981313e1959d69066"
desired_hash = 195500000
low_hash = 0

class MyClient(discord.Client):

    async def on_ready(self):
        global low_hash
        low_hash = 0
        print('Logged on as', self.user)
        channel = client.get_channel(825054534044090408)
        await channel.send('Reboot Detected!')

    async def on_message(self, message):
        # don't respond to ourselves
        # if message.author == self.user:
        #     return

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

@tasks.loop(minutes = 10)
async def check_hashrate():
    global low_hash
    channel = client.get_channel(825054534044090408)
    try:
        r = requests.get(f'https://api.ethermine.org/miner/:{address}/workers')
        found_worker = False
        
        for worker in r.json()["data"]:
            
            if worker["worker"] == "worker001":
                
                if worker["reportedHashrate"] < desired_hash:
                    low_hash+=1
                    current_hash = worker["reportedHashrate"]
                    print(f"low hash detected: {current_hash}, {low_hash} times")
                    if low_hash >= 3:
                        await channel.send(f"hash too low: {current_hash}")
                        await channel.send("screenshot")
                        await channel.send("ping")
                        os.system("shutdown -t 10 -r")
                        return
                else:
                    low_hash = 0
                    
            found_worker = True

        if found_worker == False:
            await channel.send("worker not found, rebooting")
            await channel.send("screenshot")
            await channel.send("ping")
            os.system("shutdown -t 10 -r")
    
    except requests.ConnectionError:
        print("error, no internet")

check_hashrate.add_exception_type(asyncpg.PostgresConnectionError)
check_hashrate.start()

client = MyClient()
client.run('key')
