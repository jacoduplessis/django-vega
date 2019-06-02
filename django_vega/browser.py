import json

import websockets
from urllib.request import urlopen
import asyncio
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

TIMEOUT = 1


class Browser:

    def __init__(self, host='localhost', port=9222, timeout=TIMEOUT):
        self.host = host
        self.port = port
        self.ws = None
        self.tabs = None
        self.timeout = timeout
        self.message_counter = 0
        self.listeners = defaultdict(list)
        self.results = defaultdict(asyncio.Queue)
        self.event_queue = asyncio.Queue()
        self._listen_task = None
        self._event_task = None
        self._stopped = asyncio.Event()

    def on(self, event, callback):
        self.listeners[event].append(callback)

    def off(self, event, callback):
        for cb in self.listeners[event]:
            if cb == callback:
                del self.listeners[event][cb]

    async def listen(self):

        while not self._stopped.is_set():
            try:
                payload = await self.ws.recv()
                message = json.loads(payload)
            except websockets.ConnectionClosed:
                break
            if "method" in message:
                await self.event_queue.put(message)

            elif "id" in message:
                if message["id"] in self.results:
                    await self.results[message['id']].put(message)

    async def handle_event_loop(self):
        while not self._stopped.is_set():
            event = await self.event_queue.get()
            method = event['method']
            if method not in self.listeners:
                continue
            for callback in self.listeners[method]:
                try:
                    await callback(**event['params'])
                except Exception as e:
                    logger.error("callback %s exception" % event['method'], exc_info=True)

    def get_tabs(self):
        self.tabs = json.loads(urlopen('http://{}:{}/json'.format(self.host, self.port)).read())
        print(self.tabs)

    async def call(self, method, **kwargs):
        self.message_counter += 1
        msg_id = self.message_counter
        payload = {'id': msg_id, 'method': method, 'params': kwargs}
        await self.ws.send(json.dumps(payload))

        return await asyncio.wait_for(self.results[msg_id].get(), TIMEOUT)

    async def connect(self, tab=0, update_tabs=True):
        if update_tabs or self.tabs is None:
            self.get_tabs()
        wsurl = self.tabs[tab]['webSocketDebuggerUrl']
        self.ws = await websockets.connect(wsurl, timeout=1, max_size=None)
        self._listen_task = asyncio.ensure_future(self.listen())
        self._event_task = asyncio.ensure_future(self.handle_event_loop())

    async def close(self):
        self._stopped.set()
        if self.ws:
            await self.ws.close()
        self._listen_task.cancel()
        self._event_task.cancel()

    async def wait(self, timeout=None):

        if timeout:
            try:
                await asyncio.wait_for(self._stopped.wait(), timeout)
                return True
            except asyncio.TimeoutError:
                return False

        await self._listen_task
        await self._event_task


