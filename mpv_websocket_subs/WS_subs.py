import argparse
import asyncio
import json
import sys
import time

import websockets
from python_mpv_jsonipc import MPV

# from typing import Any

# import logging

# logger = logging.getLogger("websockets")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser()
parser.add_argument("--socket")
parser.add_argument("--secondary", action="store_true", default=False)
parser.add_argument("--schema", default=None) # example: '{"sentence": "{subs}"}' where {subs} is the value received from mpv

args = parser.parse_args()
SOCKET = args.socket
secondary = args.secondary
custom_subs_json: str | None = args.schema

connections = set()

async def handler(websocket: websockets.ServerConnection) -> None:
    connections.add(websocket)
    mpv.show_text("Connected")
    try:
        async for message in websocket:
            print(message)
            if message == "stopServer":
                mpv.terminate()
                sys.exit()
    except websockets.ConnectionClosed:
        print("Client disconnected")
        mpv.show_text("Client disconnected")
    finally:
        connections.remove(websocket)


def send_subs(name: str, value: str) -> None:
    if not value:
        return
    if connections:
        temp = custom_subs_json.replace("{subs}", value) if custom_subs_json is not None else value
        loop.call_soon_threadsafe(mpvQ.put_nowait, temp)


async def monitorQ(queue: asyncio.Queue) -> None:
    while True:
        msg = await queue.get()
        for websocket in connections.copy():
            try:
                await websocket.send(msg)
            except websockets.ConnectionClosed:
                connections.discard(websocket)


async def check_connection() -> None:
    while True:
        try:
            mpv.command("client_name")
            await asyncio.sleep(5)
        except BrokenPipeError:
            print("Connection to mpv dropped. Terminating script...")
            mpv.terminate()
            sys.exit()

mpvQ = asyncio.Queue()

mpv = MPV(start_mpv=False, ipc_socket=SOCKET)

if custom_subs_json is not None:
    try:
        json.loads(custom_subs_json)
    except json.JSONDecodeError:
        print(f"Custom JSON schema '{custom_subs_json}' is not valid", flush=True)
        mpv.show_text(f"Custom JSON schema '{custom_subs_json}' is not valid")
        time.sleep(5)
        mpv.terminate()
        sys.exit()

if secondary:
    mpv.bind_property_observer("secondary-sub-text", send_subs)
else:
    mpv.bind_property_observer("sub-text", send_subs)

loop: asyncio.AbstractEventLoop # = None
# task = None


async def main() -> None:
    global loop #, mpvQ, task  # noqa: PLW0603

    loop = asyncio.get_event_loop()

    try:
        async with websockets.serve(handler, "localhost", 6677):

            mpv.show_text("WS_subs started. Connect from browser.", 60000)
            # mpvQ = asyncio.Queue()
            # main_task = asyncio.create_task(monitorQ(mpvQ))
            main_task = asyncio.gather(monitorQ(mpvQ), check_connection())
            mpv.quit_callback = main_task.cancel
            try:  # noqa: SIM105
                await main_task
            except asyncio.CancelledError:
                pass
            mpv.terminate()

    except OSError as error:
        print(error.strerror)


if __name__ == "__main__":
    asyncio.run(main())
