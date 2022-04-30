import sys
sys.path.append("packages")
import asyncio
import websockets
from Dungeon import *
import time, threading

connected = set()
clients = {} # websocket: name
threads = {} # room: thread -- used to make sure we only have one thread per room
dungeon = Dungeon()

lockRoomStates = threading.Lock() # used to avoid race conditions


##########################################################################
# Takes: string (name)
# Does: Finds the websocket address associated with a given username.
##########################################################################
def getSocketByUsername(userName):
    userNames = list(clients.values())
    index = userNames.index(userName)
    sockets = list(clients.keys())
    socket = sockets[index]

    return socket

##########################################################################
# Takes: websocket, string (name)
# Does: Adds a user to the dungeon, so long as the name given is not already
# in use.
##########################################################################
async def addUser(websocket, name):
    userNames = list(clients.values())
    if name in userNames:
        await websocket.send(f">>> That name is already taken, please choose another.")
        await websocket.send("nameTaken")
    else:
        clients[websocket] = name
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {name} has entered the dungeon. ")
            else:
                await websocket.send("validName " + name)
                await conn.send(f">>> Torch in hand, you descend down the stairwell, footsteps echoing into the long tunnel...")
                time.sleep(2)
                await conn.send(f">>> Welcome to the dungeon, {name.capitalize()}. Type help to see a list of commands.")
        dungeon.addPlayer(name)


##########################################################################
# Takes: string (room name)
# Does: As long as there are both a player and an enemy in a given room,
# a random enemy will attack a random player in the room ever 3 seconds.
##########################################################################
async def attackPlayer(room):
    enemyAttack = dungeon.playerAndEnemyInRoom(room)

    while enemyAttack:
        lockRoomStates.acquire()
        # if there is at least one player and enemy in the room
        if dungeon.playerAndEnemyInRoom(room):
            result = dungeon.attackPlayerInRoom(room)

            websocket = getSocketByUsername(result[0])
            for conn in connected:
                if conn != websocket:
                    await conn.send(f">>> {result[1]} attacked {clients[websocket]} for {result[2]} damage. ")
                    if (result[3] == "dead"):
                        await conn.send(f">>> {clients[websocket]} died!")
                else:
                    await conn.send(f">>> {result[1]} attacked you for {result[2]} damage.")
                    if (result[3] == "dead"):
                        await conn.send(f">>> You died!")
                        await conn.send("dead")
                        await conn.send(f">>> Enter restart if you wish to try again. ")

                if result[3] == "dead":
                    dungeon.removePlayer(clients[websocket])
        else: enemyAttack = False

        lockRoomStates.release()
        time.sleep(3)

    # remove thread from the dict of threads
    if (room in threads.keys()):
        del threads[room]


##########################################################################
# Takes: websocket, string (target)
# Does: Allows player to try to attack an entiry in their current room.
# Player may either try to attack another player or a random enemy in the
# room.
##########################################################################
async def attack(websocket, target):
    results = dungeon.attack(clients[websocket], target)

    # if player attacked another player
    if (len(results) == 5):
        victim = getSocketByUsername(results[2])
        for conn in connected:
            if conn == victim:
                await conn.send(f">>> {clients[websocket]} dealt {results[1]} damage to you.")
                if (results[3] == "dead"):
                    await conn.send(f">>> You died!")
                    await conn.send("dead")
                    await conn.send(f">>> Enter restart if you wish to try again. ")
            elif conn != websocket:
                await conn.send(f">>> {clients[websocket]} dealt {results[1]} damage to {results[2]}.")
                if (results[3] == "dead"):
                    await conn.send(f">>> {results[2]} died!")
            else:
                await conn.send(f">>> You dealt {results[1]} damage to {results[2]}.")
                if (results[3] == "dead"):
                    await conn.send(f">>> {results[2]} died!")

            if results[3] == "dead":
                dungeon.removePlayer(results[2])
    # if player attacked a dungeon enemy
    elif len(results) > 1:
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} dealt {results[1]} damage to the {results[2]}. The {results[2]} is {results[3]}.")
            else:
                await conn.send(f">>> You dealt {results[1]} damage to the {results[2]}. The {results[2]} is {results[3]}.")
    else:
        await websocket.send(f">>> {results[0]}")


##########################################################################
# Takes: websocket, string
# Does: Sends given message to all clients. The message sender is given
# the message for their chatlog, while all others are given the sender's
# username and message.
##########################################################################
async def chat(websocket, message):
    for conn in connected:
        if conn != websocket:
            await conn.send(f">>> {clients[websocket]}: {message} ")
        else:
            await conn.send(f">>> You: {message} ")


##########################################################################
# Takes: websocket, string (user name), string (item name)
# Does: Allows a user to try to give an item in their inventory to another
# player.
##########################################################################
async def give(websocket, target, item):
    result = dungeon.give(clients[websocket], target, item)
    if (len(result) != 1):
        await websocket.send(f">>> {result[0]}")
    else:
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} gave {target} a(n) {item}. ")
            else:
                await conn.send(f">>> You gave {target} a(n) {item}. ")


##########################################################################
# Takes: websocket, string (direction)
# Does: Allows a user to try to move to another room.
##########################################################################
async def move(websocket, direction):
    result = dungeon.move(clients[websocket], direction)

    if (len(result) == 1):
        await websocket.send(f">>> {result[0]}")
    else:
        enemyAttack = dungeon.playerAndEnemyInRoom(result[1])
        # if there is now an enemy and player in the same room, we want to make a thread
        # where the enemy attacks the player so long as they are in the room.
        # we use the threads dictionary to make sure there is only one such thread
        # per room.
        if enemyAttack and (not(result[1] in threads.keys())):
            thread = threading.Thread(target=asyncio.run, args=(attackPlayer(result[1]), ))
            thread.start()
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} moved {direction} from room {result[0]} to room {result[1]}. ")
            else:
                await conn.send(f">>> You moved {direction} from room {result[0]} to room {result[1]}. ")


##########################################################################
# Message handler.
##########################################################################
async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            elements = message.split(" ")
            command = elements[0]

            # get users added by userName
            if (command == "name"):
                await addUser(websocket, elements[1])
                # await attackPlayers(websocket)

            # player tries to attack enemy in room
            elif (command == "attack" and dungeon.isPlayerInDungeon(clients[websocket])):
                lockRoomStates.acquire()
                if len(elements) == 1:
                    await attack(websocket, None)
                else:
                    await attack(websocket, elements[1])
                lockRoomStates.release()

            # send messages to all dungeon clients
            elif (command == "chat"):
                userMessage = message[(len(command) + 1):len(message)]
                await chat(websocket, userMessage)

            # player wants to consume a health potion
            elif (command == "drink" and dungeon.isPlayerInDungeon(clients[websocket])):
                result = dungeon.drink(clients[websocket], "Potion")
                await websocket.send(f">>> {result}")

            # player wants to equip weapon
            elif (command == "equip" and dungeon.isPlayerInDungeon(clients[websocket])):
                if len(elements) < 1:
                    await websocket.send(f">>> Please choose a weapon to equip.")
                else:
                    result = dungeon.equip(clients[websocket], elements[1])
                    await websocket.send(f">>> {result}")

            # player wants to get an item in their current room
            elif (command == "get" and dungeon.isPlayerInDungeon(clients[websocket])):
                if len(elements) < 1:
                    await websocket.send(f">>> An item name must be given. Items include knife, sword, dagger, and potion.")
                else:
                    result = dungeon.get(clients[websocket], elements[1])
                    resultParsed = result.split(" ")
                    if (resultParsed[0] == "Item"):
                        await websocket.send(f">>> {result}")
                    else:
                        await websocket.send(f">>> {result}")

            # player wants to give another player an item
            elif (command == "give" and dungeon.isPlayerInDungeon(clients[websocket])):
                if len(elements) < 2:
                    await websocket.send(f">>> You must specify a player and an item.")
                else:
                    await give(websocket, elements[1], elements[2])

            # player wants information on a given item
            elif (command == "info"):
                result = dungeon.info(elements[1])
                await websocket.send(f">>> {result}")

            # player wants to know what's in their current room.
            elif (command == "look" and dungeon.isPlayerInDungeon(clients[websocket])):
                result = dungeon.look(clients[websocket])
                for line in reversed(result):
                    await websocket.send(f">>> {line}")

            # move player
            elif (command == "move" and dungeon.isPlayerInDungeon(clients[websocket])):
                lockRoomStates.acquire()
                if len(elements) < 1:
                    await websocket.send(f">>> A direction must be given. You can move north, east, south, or west.")
                else:
                    direction = elements[1]
                    await move(websocket, direction)
                lockRoomStates.release()

            # player wants to know who else is in the dungeon
            elif (command == "players"):
                currentPlayers = dungeon.players()
                await websocket.send(f">>> {currentPlayers}")

            # player is restarting the game
            elif (command == "restart"):
                lockRoomStates.acquire()
                if (dungeon.isPlayerInDungeon(clients[websocket])):
                    dungeon.removePlayer(clients[websocket])
                dungeon.addPlayer(clients[websocket])
                lockRoomStates.release()
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f">>> {clients[websocket]} restarted at the entrance. ")
                    else:
                        await conn.send(f">>> You restart at the entrance. ")

            # player wants to know their current status
            elif (command == "self" and dungeon.isPlayerInDungeon(clients[websocket])):
                result = dungeon.self(clients[websocket]).split(". ")
                await websocket.send(f">>> === Self ===")
                await websocket.send(f">>> HP: {result[0]}")
                await websocket.send(f">>> Equipped weapon: {result[1]}")
                await websocket.send(f">>> {result[2]}")
                await websocket.send(f">>> {result[3]}")
                await websocket.send(f">>> ============")

            else:
                await websocket.send(f">>> Command given not recognized. Type help to see commands. ")

            # for debugging
            print(f">>> {message}")

    finally:
        dungeon.removePlayer(clients[websocket])
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} has left the dungeon. ")
        # Unregister.
        connected.remove(websocket)
        if websocket in clients:
            del clients[websocket]


# for connecting on local host
start_server = websockets.serve(server, "localhost", 5000)
# for connecting on local network, replace IP
# start_server = websockets.serve(server, IP, 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
