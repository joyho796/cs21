import asyncio
import websockets
from Dungeon import *

# debugging needs:
# make sure there are no duplicate usernames, and only send to users with
# usernames

connected = set()
clients = {} # websocket: name
userNames = []
dungeon = Dungeon()

async def addUser(websocket, name):
    clients[websocket] = name
    for conn in connected:
        if conn != websocket:
            await conn.send(f">>> {name} has entered the dungeon. ")
        else:
            await conn.send(f">>> Welcome to the dungeon, {name}!")
    dungeon.addPlayer(name)


async def chat(websocket, message):
    for conn in connected:
        if conn != websocket:
            await conn.send(f">>> {clients[websocket]}: {message} ")
        else:
            await conn.send(f">>> You: {message} ")


async def move(websocket, message, direction):
    result = dungeon.handleMessage(clients[websocket], message)

    if (result == "There's no room over there"):
        await websocket.send(f">>> {result}")
    else:
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} moved {direction} to room {result}. ")
            else:
                await conn.send(f">>> You moved {direction} to room {result}. ")


# needs work
async def attack(websocket, message):
    result = dungeon.handleMessage(clients[websocket], message)
    if (result.split(" ")[0] == "dealt"):
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} dealt {result} damage to enemy.")
            else:
                await conn.send(f">>> You dealt {result} damage to enemy. ")
    else:
        await websocket.send(result)


async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            elements = message.split(",")
            command = elements[0]

            # get users added by userName
            if (command == "name"):
                await addUser(websocket, elements[1])

            # send messages to all dungeon clients
            elif (command == "chat"):
                userMessage = message[(len(command) + 1):len(message)]
                await chat(websocket, userMessage)

            # move player
            elif (command == "move"):
                direction = elements[1]
                await move(websocket, message, direction)

            # player tries to attack enemy in room
            elif (command == "attack"):
                await attack(websocket, message)

            # player wants to know who else is in the dungeon
            elif (command == "players"):
                currentPlayers = dungeon.getPlayers()
                await websocket.send(f">>> {currentPlayers}")

            # player wants to know what's in their current room.
            elif (command == "look"):
                result = dungeon.handleMessage(clients[websocket], "look")
                for line in reversed(result):
                    await websocket.send(f">>> {line}")

            elif (command == "info"):
                result = dungeon.handleMessage(clients[websocket], message)
                await websocket.send(f">>> {result}")

            elif (command == "get"):
                result = dungeon.handleMessage(clients[websocket], message)
                resultParsed = result.split(" ")
                if (resultParsed[0] == "Item"):
                    await websocket.send(f">>> {result}")
                else:
                    await websocket.send(result)

            elif (command == "drink"):
                result = dungeon.handleMessage(clients[websocket], message)
                await websocket.send(result)

            # leaving this here for debugging purposes
            else:
                for conn in connected:
                    await conn.send(">>> Succesfully pushed button")

            # for debugging
            print(f">>> {message}")
    finally:
        # Unregister.
        connected.remove(websocket)


start_server = websockets.serve(server, "localhost", 5000)
#start_server = websockets.serve(server, "169.254.219.144", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
