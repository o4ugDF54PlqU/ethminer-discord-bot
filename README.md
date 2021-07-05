# ethminer-discord-bot
A discord bot that interfaces with the ethminer API and Hiveon/Ethermine to allow for remote monitoring and control through discord. The bot will be run on the mining rig - if you have multiple each rig will have a single bot. 

I wrote this on and for Windows and ethminer, so other platforms and miners will require tweaking.

Don't forget to put in your bot key from discord.

# Setup
1. Install python 3
1. Install dependencies with setup.py or manually
1. Create a bot and get its key (https://www.writebots.com/discord-bot-token/)
1. Add the bot to your server, it should now show up as offline
1. Chose which pool and version you want to run and download it
    1. multi is if you want to have multiple bots/rigs controllable in one channel
    1. if you don't want to use either pool, just select one and set check_enabled to False
1. Open the downloaded bot and change the settings
    - key is your bot key from the previous steps (not your invite link)
    - notification_channel is the channel in your server you want to be notified in (you can still send commands from other channels, and it would reply to those commands in those channels). For example, opening a channel on discord web would give you https://discord.com/channels/311480678468550624/825054534044090408 and 825054534044090408 would be the channel number you need.
    - check_enabled enables periodic pool hashrate checks and automatic pings.
    - address is your eth wallet address
    - desired_hash is the threshold hashrate under which the bot will reboot the mining rig 
    - times_to_check is the number of consecutive times the pool hashrate must be below desired_hash before rebooting, just to make sure (note: pool apis update once every 10 minutes)
    - worker_name is the name of your worker, same as the one set in ethminer
1. To get the "ping" command to work correctly, you'll need to install wkhtmltopdf for imgkit. Instructuctions: https://pypi.org/project/imgkit/
1. Add the bot to the startup folder/task scheduler
    - If you want to hide the bot window, simply rename the script extension from .py to .pyw
1. **Make sure to put --api-bind 127.0.0.1:3333 in your ethminer script**

# Features:
- Sends a message to a predetermined channel on reboot (useful to know when a power outage happens or keep track of instability)
- Replies to "ping" with data
- Pings itself every 10 minutes by default (I recommend disabling notification on that channel)
- Remote rebooting with "reboot" and "force reboot"
- Replies to "screenshot" with a screenshot - useful if you keep temperature data for AMD on the screen for example
- Checks with pool API every 10 minutes. If hashrate lower than limit times_to_check times in a row, @everyone, reboot and send screenshot for diagnostic.
    - Also does a ping every check. Simply delete if you don't want periodic data.
- For the multi versions, simply add the worker name in front of each command (eg "worker001 reboot")
- Bonus: ethermine calculator, calculates 24h shares because the default 1h is dumb

![image](https://user-images.githubusercontent.com/36900762/115118918-e725e880-9fcf-11eb-87a4-a74c10ae2ff7.png)

