""" Basic web socket server. """
import asyncio
from contextlib import suppress
import websockets


class Server:
    """ Web socket server managing multiple connections. """

    def __init__(self):
        """
        sockets = {
            co_id: {
                ws: ..., # the ws instance for client co.
                path: ..., # end point requested.
                msg: [] # msg from client.
        }}
        """
        self.co_id = 0  # increment on each connection
        self.sockets = {}
        self._close_event = asyncio.Event()
        self._server = None

    @classmethod
    async def create(cls, port, host="127.0.0.1"):
        """ Get new WsServer instance. """
        wsserver = cls()
        wsserver._server = await websockets.serve(wsserver.co_handler, host, port)
        return wsserver

    def close(self):
        """ Shutdown. """
        self._close_event.set()

    async def wait_closed(self):
        """ Wait until the server is closed. """
        await self._close_event.wait()

        async def stop_task(task):
            if task and not task.done():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    await task

        await asyncio.gather(*[stop_task(sock["_msg_handler_task"])
                               for sock in self.sockets.values()])

        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()

    async def co_handler(self, websocket, path):
        """ New connection handler. """
        self.co_id += 1
        task_started_event = asyncio.Event()
        task = asyncio.ensure_future(self.msg_handler(self.co_id, websocket, task_started_event))
        self.sockets[self.co_id] = {
            "ws": websocket,
            "path": path,
            "msg": [],
            "_msg_handler_task": task
        }
        await task_started_event.wait()
        # block until server close
        await self._close_event.wait()

    async def msg_handler(self, co_id, websocket, task_started_event):
        """ Background coro for new message handler. """
        task_started_event.set()
        async for message in websocket:
            self.sockets[co_id]["msg"].append(message)
        # client quit, task done.

    async def send_to_clients(self, msg):
        """ Send a message to all clients. """
        for sock in self.sockets.values():
            try:
                await sock["ws"].send(msg)
            except websockets.exceptions.ConnectionClosed:
                # client disconnected
                pass
