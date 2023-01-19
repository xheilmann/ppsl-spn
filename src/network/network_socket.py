from functools import partial
import sys

from src import websockets
from src.globals import (
    IDs,
    Keys,
    Values,
)
import threading

import asyncio
import time
from datetime import datetime

import json

import logging

logger = logging.getLogger(__name__)

import nest_asyncio

nest_asyncio.apply()


class NetworkSocket:
    def __init__(self, member) -> None:
        self.member = member
        self.id_chip = member.id_chip
        self.isReady = False
        self.stop = False
        self.__latency = int(
            self.member.config[f"ID_{self.id}"].get(Keys.CONFIG_LATENCY)
        )

        self.server_thread = threading.Thread(target=self.__thread_start_server)
        self.server_thread.start()

    @property
    def id(self):
        return self.id_chip.id

    @property
    def ip4(self):
        return self.id_chip.ip4

    @property
    def port(self):
        return self.id_chip.port

    @property
    def name(self):
        return f"{self.id_chip.name}s_NetworkSocket"

    @property
    def latency(self):
        return self.__latency

    def __thread_start_server(self):
        logger.info_spn(f"Server-thread for {self.id} started")
        asyncio.run(self.__start_server(self.ip4, self.port))

    def __start_server(self, ip4, port):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        start_server = websockets.serve(self.__receive, ip4, port, loop=event_loop)
        logger.info_spn(
            f"Websockets server for {self.id} listening to {self.ip4}:{self.port}"
        )
        event_loop.run_until_complete(start_server)
        self.isReady = True
        self.member.on_ready()
        event_loop.run_forever()

    async def __receive(self, websocket, path):
        async for message in websocket:
            # message_json_str = await websocket.recv()
            # message = json.loads(message_json_str)
            message = json.loads(message)
            # if not (self.id is Values.MANAGER_ID):
            # time.sleep(self.latency / 1000)
            self.member.evaluate_message(message)

        # message_json_str = await websocket.recv()
        # message = json.loads(message_json_str)
        # if not (self.id is Values.MANAGER_ID):
        #    time.sleep(self.latency / 1000)
        # self.member.evaluate_message(message)
        # await websocket.send(message_json_str)  ###

    def send(self, target_id_chip, data_id, value):
        while not self.isReady:
            time.sleep(1)
        # asyncio.new_event_loop().run_until_complete(
        #    self.__send(target_id_chip, data_id, value)
        # )
        # if self.id is Values.MANAGER_ID:
        #    asyncio.get_event_loop().call_soon(partial(print, "Manager send", flush=True))

        asyncio.get_event_loop().run_until_complete(
            self.__send(target_id_chip, data_id, value)
        )

    async def __send(self, target_id_chip, data_id, data_value):

        target_ip4 = target_id_chip.ip4
        target_port = target_id_chip.port
        uri = f"ws://{target_ip4}:{target_port}"
        async with websockets.connect(uri) as websocket:
            ##start_time = time.time()
            source = {}
            source["ip4"] = self.ip4
            source["port"] = self.port

            data = {}
            data["id"] = data_id
            data["value"] = data_value

            message = {}
            message["source"] = source
            message["data"] = data

            message_json_str = json.dumps(message)
            logger.debug_spn_communication(
                f"{datetime.now()}: sending from {self.ip4}:{self.port} to {target_ip4}:{target_port} message {data_id}:{data_value}"
            )

            if target_id_chip.id is Values.MANAGER_ID:
                time.sleep(self.latency / 1000)

            await websocket.send(message_json_str)
            # await websocket.recv()  ####
            ##end_time = time.time()
            ##self.member.table_time += end_time - start_time
