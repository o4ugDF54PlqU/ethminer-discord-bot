# ethminer-discord-bot
A discord bot that interfaces with the ethminer API and Hiveon/Ethermine to allow for remote monitoring and control through discord. Will require a fair bit of setup. Don't forget to put in your bot key.

# Setup

To get the "ping" command to work correctly, you'll need to install wkhtmltopdf for imgkit. Instructuctions:
https://pypi.org/project/imgkit/

# Features:
- Sends a message to a predetermined channel on reboot (useful to know when a power outage happens and you need to reapply overclocks)
- Replies to "ping" with data
- Remote shutdown with "reboot" and "force reboot"
- Replies to "screenshot" with a screenshot
- Checks with pool API every 10 minutes to see hashrate. If hashrate lower than limit 3 times in a row, reboot

![image](https://user-images.githubusercontent.com/36900762/115118918-e725e880-9fcf-11eb-87a4-a74c10ae2ff7.png)

