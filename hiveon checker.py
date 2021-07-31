import json
import requests
import time
import os

# pool hash check, reboot if hash lower than desired_hash times_to_check times in a row
address = "696b18d7e003be5b4d1a66b981313e1959d69066"
desired_hash = 169000000
times_to_check = 3
worker_name = "WORKER001" # note: case sensitive

desired_log = []

time.sleep(60)

while times_to_check > 0:
    time.sleep(600)
    try:
        r = requests.get(f'https://hiveon.net/api/v1/stats/miner/{address}/ETH/workers')
        worker_data = r.json()["workers"][worker_name]
        
        if int(worker_data["reportedHashrate"]) < desired_hash:
            current_hash = r.json()["reportedHashrate"]
            print(f"low hash detected: {current_hash}")
            desired_log.append(False)
        else:
            print("satisfactory hashrate")
            desired_log.append(True)

    except requests.ConnectionError:
        print("error, no internet")
        times_to_check -= 1
        desired_log.append(False)
    except KeyError:
        print("not in pool")
        desired_log.append(False)
    
    times_to_check -= 1

if any(desired_log):
    print("satisfactory")
else:
    os.system("shutdown -t 10 -r")