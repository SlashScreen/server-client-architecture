#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
from guizero import App, Text

logging.basicConfig()

messages = []

USERS = set()

#app = App(title="IRC")
#message = Text(app, text="Welcome to the IRC server screen!")
#allmessages = Text(app,text="yo")
#app.display()

def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
 #   await register(websocket)
    msg = await websocket.recv()
    print(msg)
    messages.append(msg)
    #await websocket.send('\n'+msg)
 #   await unregister(websocket)

start_server = websockets.serve(counter, 'localhost', 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
