import logging
import time
from concurrent.futures import as_completed, Future
from typing import List, Dict
import requests
from concurrent.futures import ThreadPoolExecutor

from src.constants import *
from src.server import Server

logger = logging.getLogger(LB_LOGGER)


class LoadBalancer:
    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.pointer = 0
        self.servers_length = len(servers)
        self.start_health_check()

    def start_health_check(self):
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.health_check_ticker)          

    def get_servers(self):
        return self.servers

    def get_server_by_idx(self, idx) -> Server:  
        assert (0 <= idx < self.servers_length)
        return self.servers[idx]

    def get_next_server(self) -> str:
        start_time = time.time()

        while not self.servers[self.pointer].is_healthy:
            self.pointer = (self.pointer + 1) % self.servers_length

            # Timeout check - avoid infinite loop
            if time.time() - start_time > SERVER_LOOKUP_TIMEOUT:
                return ""

        chosen = self.servers[self.pointer]
        self.pointer = (self.pointer + 1) % self.servers_length
        return chosen.endpoint

    def health_check_ticker(self):
        while True:
            with ThreadPoolExecutor(max_workers=MAX_SERVERS) as executor:
                future_to_server: Dict[Future, str] = {
                    executor.submit(self.is_server_up, server): server for server in self.servers
                }
                for future in as_completed(future_to_server):
                    future.result()
                time.sleep(HEALTH_CHECK_PERIOD)

    @staticmethod
    def is_server_up(server: Server):
        try:
            response = requests.get(server.endpoint, timeout=5)
            server.is_healthy = response.status_code == 200
        except requests.exceptions.RequestException:
            server.is_healthy = False
        finally:
            logger.info(server)
