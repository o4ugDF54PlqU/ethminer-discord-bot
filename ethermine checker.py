import json
import requests
import time
import os

# pool hash check, reboot if hash lower than desired_hash times_to_check times in a row
address = "696b18d7e003be5b4d1a66b981313e1959d69066"
desired_hash = 169000000
times_to_check = 3
worker_name = "worker001" # I don't think it's case sensitive

desired_log = []

time.sleep(60)

while times_to_check > 0:
    time.sleep(600)
    try:
        r = requests.get(f'https://api.ethermine.org/miner/:{address}/workers')
        found_worker = False
        
        for worker in r.json()["data"]:
            
            if worker["worker"] == worker_name:
                
                if worker["reportedHashrate"] < desired_hash:
                    current_hash = worker["reportedHashrate"]
                    print(f"low hash detected: {current_hash}")
                    desired_log.append(False)

                else:
                    print("satisfactory hashrate")
                    desired_log.append(True)
                    
                found_worker = True
                break

        if found_worker == False:
            print("worker not found on pool")
            desired_log.append(False)

    except requests.ConnectionError:
        print("error, no internet")
        times_to_check -= 1
        desired_log.append(False)
    except AttributeError:
        print("not logged on yet")
        desired_log.append(False)
    
    times_to_check -= 1

if any(desired_log):
    print("satisfactory")
else:
    os.system("shutdown -t 10 -r")