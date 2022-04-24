import asyncio
import websockets
from DungeonTest import *

# debugging needs:
# make sure there are no duplicate usernames, and only send to users with
# usernames

connected = set()
clients = {} # websocket: name
dungeon = Dungeon()

def getUserMessage(message, command):
    return message[(len(command) + 1):len(message)]

async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            elements = message.split(",")
            command = elements[0]
            userMessage = getUserMessage(message, command)

            # get users added by userName
            if (command == "name"):
                clients[websocket] = elements[1]
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f">>> {elements[1]} has entered the dungeon. ")
                    else:
                        await conn.send(f">>> Welcome to the dungeon, {elements[1]}!")
                        introMessage = dungeon.getIntro()
                        await conn.send(f">>> {introMessage}")
                dungeon.addPlayer(elements[1])

            elif (command == "chat"):
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f">>> {clients[websocket]}: {userMessage} ")
                    else:
                        await conn.send(f">>> You: {userMessage} ")

            elif (command == "move"):
                direction = elements[1]
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f">>> {clients[websocket]} moved {direction}. ")
                    else:
                        await conn.send(f">>> You moved {direction}. ")

            elif (command == "attack"):
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f">>> {clients[websocket]} attacked. ")
                    else:
                        await conn.send(f">>> You attacked. ")


            elif (command == "players"):
                currentPlayers = dungeon.getPlayers()
                await websocket.send(f">>> {currentPlayers}")

            # leaving this here for debugging purposes
            else:
                for conn in connected:
                    await conn.send(">>> Succesfully pushed button")

            print(f">>> {message}")
    finally:
        # Unregister.
        connected.remove(websocket)



start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
