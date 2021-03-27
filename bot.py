import discord
import json
import requests
import imgkit
# GPU information
import GPUtil

ping_data = {
  "id": 1,
  "jsonrpc": "2.0",
  "method": "miner_getstatdetail"
}

data_json = json.dumps(ping_data)
payload = {'json_payload': data_json}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        channel = client.get_channel(825054534044090408) #insert your channel here
        await channel.send('Reboot Detected!')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
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

            text_list = []
            for item in list_gpus:
                text_list.append('\t\t'.join(item))

            text = '\n'.join(text_list)
            await message.channel.send("```"+text+"```")

client = MyClient()
client.run('key')
