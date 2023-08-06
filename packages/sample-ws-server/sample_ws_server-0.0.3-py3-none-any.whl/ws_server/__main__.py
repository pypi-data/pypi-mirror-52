""" Entry point for ws-server. """
import argparse
import asyncio
from functools import partial
import signal
import logging
from .server import Server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Server host",
                        default="127.0.0.1")
    parser.add_argument("--port", help="Port to bind",
                        default="3000",
                        type=int)
    parser.add_argument("--verbosity", help="Log level DEBUG|INFO|WARNING...",
                        default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=args.verbosity.upper())

    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(Server.create(host=args.host,
                                                   port=args.port))

    # Register signal handlers
    def shutdown(sig):
        server.close()

    loop.add_signal_handler(signal.SIGINT, partial(shutdown, "SIGINT"))
    loop.add_signal_handler(signal.SIGTERM, partial(shutdown, "SIGTERM"))

    # Run service
    loop.run_until_complete(server.wait_closed())
    loop.remove_signal_handler(signal.SIGINT)
    loop.remove_signal_handler(signal.SIGTERM)
    loop.close()


if __name__ == '__main__':
    main()
