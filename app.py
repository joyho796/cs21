import asyncio
import websockets
from Dungeon import *
import time

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
            await conn.send(f">>> Welcome to the dungeon, {name}! Type help to see a list of commands.")
    dungeon.addPlayer(name)

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
    results = result.split(" ")
    if results[0] != "There's":
        for conn in connected:
            if conn != websocket:
                await conn.send(f">>> {clients[websocket]} dealt {results[0]} damage to enemy. Enemy is {results[1]}.")
            else:
                await conn.send(f">>> You dealt {results[0]} damage to enemy. Enemy is {results[1]}.")
    else:
        await websocket.send(f">>> {result}")


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
                # await attackPlayers(websocket)

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
                    await websocket.send(f">>> {result}")

            elif (command == "drink"):
                result = dungeon.handleMessage(clients[websocket], message)
                await websocket.send(f">>> {result}")

            # leaving this here for debugging purposes
            elif (command == "self"):
                result = dungeon.handleMessage(clients[websocket], message).split(". ")
                await websocket.send(f">>> HP: {result[0]}")
                await websocket.send(f">>> Equipped weapon: {result[1]}")
                await websocket.send(f">>> {result[2]}")
                await websocket.send(f">>> {result[3]}")

            elif (command == "equip"):
                result = dungeon.handleMessage(clients[websocket], message)
                await websocket.send(f">>> {result}")
            else:
                for conn in connected:
                    await conn.send("Succesfully pushed button")

            # for debugging
            print(f">>> {message}")
    finally:
        # Unregister.
        connected.remove(websocket)
        if websocket in clients:
            del clients[websocket]


start_server = websockets.serve(server, "localhost", 5000)
#start_server = websockets.serve(server, "169.254.219.144", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
