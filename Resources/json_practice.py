import json as js

player = {}
p1_board = [[ (0,1) for x in range(7)] for y in range(7)]

# board setup
request = {}
request['game_id'] = 3
request['player'] = "andrew"
request['req_type'] = 'board_setup'
request['req'] = p1_board
test = js.dumps(request)
print(test)
dec = js.loads(test)
print(dec['req'][3][4])
# move
request['game_id'] = 3
request['player'] = "andrew"
request['req_type'] = 'move'
request['req'] = (5,1)
test = js.dumps(request)
print(test)
dec = js.loads(test)
print(dec['req'])
# join game
request['player'] = "andrew"
request['req_type'] = 'join_game'
request['req'] = 1
test = js.dumps(request)
print(test)
dec = js.loads(test)
print(dec['req'])

dec = js.loads(test)
