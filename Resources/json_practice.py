import json as js

player = {}


player["name"] = "andrew"
player["pos"] = (2,1)
player["type"] = "shot"

test = js.dumps(player)

print(test)

dec = js.loads(test)

print(dec["type"])