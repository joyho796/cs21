import asyncio
import websockets
from Dungeon import *
import time, threading

# debugging needs:
# make sure there are no duplicate usernames, and only send to users with
# usernames

connected = set()
clients = {} # websocket: name
userNames = []
threads = {}
dungeon = Dungeon()

async def addUser(websocket, name):
    clients[websocket] = name
    for conn in connected:
        if conn != websocket:
            await conn.send(f">>> {name} has entered the dungeon. ")
        else:
            #intro = dungeon.getIntro()
            #for line in intro:
            #    await conn.send(f"intro >>> {line}")
            await conn.send(f">>> Welcome to the dungeon, {name}! Type help to see a list of commands.")
    dungeon.addPlayer(name)


# player wants to attack an enemy in the room
async def attack(websocket, target):
    results = dungeon.attack(clients[websocket], target)


    if (len(results) == 3):
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} dealt {results[1]} damage to {results[2]}.")
            else:
                await conn.send(f">>> You dealt {results[1]} damage to {results[2]}.")
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


async def attackPlayers(websocket):
    while True:
        time.sleep(5)
        result = dungeon.handleMessage(clients[websocket], "attackPlayer")
        for conn in connected:
            if conn == websocket:
                await conn.send(f">>> {result}")

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

async def move(websocket, direction):
    result = dungeon.move(clients[websocket], direction)
    print(result)

    if (len(result) == 1):
        await websocket.send(f">>> {result[0]}")
    else:
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} moved {direction} from room {result[0]} to room {result[1]}. ")
            else:
                await conn.send(f">>> You moved {direction} from room {result[0]} to room {result[1]}. ")


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
            elif (command == "attack"):
                if len(elements) == 1:
                    await attack(websocket, None)
                else:
                    await attack(websocket, elements[1])

            # send messages to all dungeon clients
            elif (command == "chat"):
                userMessage = message[(len(command) + 1):len(message)]
                await chat(websocket, userMessage)

            # player wants to consume a health potion
            elif (command == "drink"):
                result = dungeon.drink(clients[websocket])
                await websocket.send(f">>> {result}")

            # player wants to equip weapon
            elif (command == "equip"):
                if len(elements) < 1:
                    await websocket.send(f">>> Please choose a weapon to equip.")
                else:
                    result = dungeon.equip(clients[websocket], elements[1])
                    await websocket.send(f">>> {result}")

            # player wants to get an item in their current room
            elif (command == "get"):
                if len(elements) < 1:
                    await websocket.send(f">>> An item name must be given. Items include knife, sword, dagger, and potion.")
                else:
                    result = dungeon.get(clients[websocket], elements[1])
                    resultParsed = result.split(" ")
                    if (resultParsed[0] == "Item"):
                        await websocket.send(f">>> {result}")
                    else:
                        await websocket.send(f">>> {result}")

            # player wants information on a given item
            elif (command == "info"):
                result = dungeon.info(elements[1])
                await websocket.send(f">>> {result}")

            # player wants to know what's in their current room.
            elif (command == "look"):
                result = dungeon.look(clients[websocket])
                for line in reversed(result):
                    await websocket.send(f">>> {line}")

            # move player
            elif (command == "move"):
                if len(elements) < 1:
                    await websocket.send(f">>> A direction must be given. You can move north, east, south, or west.")
                else:
                    direction = elements[1]
                    await move(websocket, direction)

            # player wants to know who else is in the dungeon
            elif (command == "players"):
                currentPlayers = dungeon.players()
                await websocket.send(f">>> {currentPlayers}")

            # player wants to know their current status
            elif (command == "self"):
                result = dungeon.self(clients[websocket]).split(". ")
                await websocket.send(f">>> === Self ===")
                await websocket.send(f">>> HP: {result[0]}")
                await websocket.send(f">>> Equipped weapon: {result[1]}")
                await websocket.send(f">>> {result[2]}")
                await websocket.send(f">>> {result[3]}")

            elif (command == "give"):
                if len(elements) < 2:
                    await websocket.send(f">>> You must specify a player and an item.")
                else:
                    await give(websocket, elements[1], elements[2])

            else:
                await websocket.send(f">>> Command given not recognized. Type help to see commands. ")

            # for debugging
            print(f">>> {message}")

    finally:
        dungeon.removePlayer(clients[websocket])
        for conn in connected:
            if conn != websocket:
                await conn.send(f"{clients[websocket]} has left the dungeon. ")
        # Unregister.
        connected.remove(websocket)
        if websocket in clients:
            del clients[websocket]


start_server = websockets.serve(server, "localhost", 5000)
#start_server = websockets.serve(server, "169.254.219.144", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
