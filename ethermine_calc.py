import requests

address = "696b18d7e003be5b4d1a66b981313e1959d69066"
r = requests.get(f'https://api.ethermine.org/miner/:{address}/history')

total_valid = 0
total_stale = 0
total_invalid = 0
for time in r.json()["data"]:
    total_valid += time["validShares"]
    total_stale += time["staleShares"]
    total_invalid += time["invalidShares"]

print(f"percent valid:{total_valid}/{total_valid+total_invalid+total_stale}, {100*total_valid/(total_valid+total_invalid+total_stale)}")
print(f"percent stale:{total_stale}/{total_valid+total_invalid+total_stale}, {100*total_stale/(total_valid+total_invalid+total_stale)}")
print(f"percent invalid:{total_invalid}/{total_valid+total_invalid+total_stale}, {100*total_invalid/(total_valid+total_invalid+total_stale)}")