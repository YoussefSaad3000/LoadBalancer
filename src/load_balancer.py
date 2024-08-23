import time
from concurrent.futures import as_completed, Future
from typing import List, Dict

import requests
from concurrent.futures import ThreadPoolExecutor


HEALTH_CHECK_PERIOD = 10
MAX_SERVERS = 5


class Server:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.is_healthy = False

    @staticmethod
    def get_servers_from_endpoints(endpoints):
        return list(Server(endpoint) for endpoint in endpoints)

    def __str__(self):
        return f"endpoint: {self.endpoint}, is_health: {self.is_healthy}"


class LoadBalancer:

    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.pointer = 0
        self.health_check_ticker()

    def get_next_server(self):
        chosen = self.servers[self.pointer]
        self.pointer = (self.pointer+1) % len(self.servers)
        return chosen.endpoint

    @staticmethod
    def is_server_up(server: Server):
        try:
            response = requests.get(server.endpoint, timeout=5)
            # Check if the status code is 200 (OK)
            server.is_healthy = response.status_code == 200
        except requests.exceptions.RequestException:
            # Catch any network-related errors
            server.is_healthy = False
        finally:
            print(server)

    def health_check_ticker(self):
        while True:
            with ThreadPoolExecutor(max_workers=MAX_SERVERS) as executor:
                future_to_server: Dict[Future, str] = {
                    executor.submit(self.is_server_up, server): server for server in self.servers
                }
                for future in as_completed(future_to_server):
                    future.result()
                time.sleep(HEALTH_CHECK_PERIOD)
