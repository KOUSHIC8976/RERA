             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from __future__ import annotations

import argparse
import asyncio
import asyncio.streams
import json
import os
import socket
import subprocess
import time
from typing import Optional, Set

from smarts.core import config
from smarts.core.utils.networking import find_free_port
from smarts.core.utils.sumo_utils import SUMO_PATH


class CentralizedTraCIServer:
    """A centralized server for handling SUMO instances to prevent race conditions."""

    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port

        self._used_ports: Set[int] = set()
        self._last_client: float = time.time()

    async def start(self, timeout: Optional[float] = 60.0 * 60.0):
        """Start the server."""
                                
        server = await asyncio.start_server(self.handle_client, self._host, self._port)

        address = server.sockets[0].getsockname()
        print(f"Server listening on `{address = }`")
        async with server:
            waitable = server.serve_forever()
            if timeout is not None:
                _timeout_watcher = asyncio.create_task(self._timeout_watcher(timeout))
                waitable = asyncio.gather(waitable, _timeout_watcher)
            await waitable

    async def _timeout_watcher(self, timeout: float):
        """Closes the server if it is not in use for `timeout` length of time."""

        while True:
            await asyncio.sleep(60)
            if time.time() - self._last_client > timeout and len(self._used_ports) == 0:
                print(f"Closing because `{timeout=}` was reached.")
                loop = asyncio.get_event_loop()
                loop.stop()

    async def _process_manager(self, binary, args, f: asyncio.Future):
        """Manages the lifecycle of the TraCI server."""
        _sumo_proc = None
        _port = None
        try:
                                         
            while (_port := find_free_port()) in self._used_ports:
                pass
            self._used_ports.add(_port)
            _sumo_proc = await asyncio.create_subprocess_exec(
                *[
                    os.path.join(SUMO_PATH, "bin", binary),
                    f"--remote-port={_port}",
                ],
                *args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            f.set_result(
                {
                    "port": _port,
                    "future": future,
                }
            )

            result = await asyncio.wait_for(future, None)
        finally:
            if _port is not None:
                self._used_ports.discard(_port)
            if _sumo_proc is not None and _sumo_proc.returncode is None:
                _sumo_proc.kill()
            self._last_client = time.time()

    async def handle_client(self, reader, writer):
        """Read data from the client."""
        address = writer.get_extra_info("peername")
        print(f"Received connection from {address}")
        loop = asyncio.get_event_loop()
        try:
            port = None
            _traci_server_info = None
            while True:
                data = await reader.readline()
                message = data.decode("utf-8")
                                                            
                if message.startswith("sumo"):
                    kill_f = loop.create_future()
                    sumo_binary, _, sumo_cmd = message.partition(":")
                    response_list = json.loads(sumo_cmd)
                    command_args = [
                        *response_list,
                    ]
                    asyncio.create_task(
                        self._process_manager(sumo_binary, command_args, kill_f)
                    )
                    if _traci_server_info is not None:
                        print("Duplicate start request received.")
                        continue
                    _traci_server_info = await asyncio.wait_for(kill_f, None)
                    port = _traci_server_info["port"]

                    response = f"{self._host}:{port}"
                    print(f"Send TraCI address: {response!r}")
                    writer.write(response.encode("utf-8"))

                if message.startswith("e:"):
                    if _traci_server_info is None:
                        print("Kill received for uninitialized process.")
                    else:
                        _traci_server_info["future"].set_result("kill")
                    break
                if len(message) == 0:
                    break

                                  
            await writer.drain()
            writer.close()
        except asyncio.CancelledError:
                                      
            pass


def spawn_if_not(remote_host: str, remote_port: int):
    """Create a new server if it does not already exist.

    Args:
        remote_host (str): The host name.
        remote_port (int): The host port.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((remote_host, remote_port))
    except (OSError):
        if remote_host in ("localhost", "127.0.0.1"):
            command = [
                "python",
                "-m",
                __name__,
                "--timeout",
                "600",
                "--port",
                remote_port,
            ]

                                                                         
            _ = subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
                close_fds=True,
            )

    else:
        client_socket.close()


def main(*_, _host=None, _port=None, timeout: Optional[float] = 10 * 60):
    """The program entrypoint."""
                                                              
    _host = _host or config()(
        "sumo", "central_host"
    )                                                       
    _port = _port or config()("sumo", "central_port")

    ss = CentralizedTraCIServer(_host, _port)
    asyncio.run(ss.start(timeout=timeout))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument(
        "--timeout",
        help="Duration of time until server shuts down if not in use.",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--port",
        help="The port to host on.",
        type=int,
        default=None,
    )
    args = parser.parse_args()

    main(_port=args.port, timeout=args.timeout)
