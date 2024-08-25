import time
from concurrent.futures import as_completed, Future
from typing import List, Dict
import signal

import requests
from concurrent.futures import ThreadPoolExecutor


HEALTH_CHECK_PERIOD = 10
MAX_SERVERS = 5
SERVER_LOOKUP_TIMEOUT = 20

def timeout_handler(signum, frame):
    raise TimeoutException

class TimeoutException(Exception):
    pass



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
        self.servers_lenght =  len(servers)
        self.set_health_checker()

    def set_health_checker(self):
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.health_check_ticker)          

    def get_servers(self):
        return self.servers

    def get_server_by_idx(self, idx) -> Server:  
        assert (0<= idx < self.servers_lenght)
        return self.servers[idx]


    def get_next_server(self) -> str:
        start_time = time.time()

        while not self.servers[self.pointer].is_healthy:
            self.pointer = (self.pointer + 1) % self.servers_lenght
            
            # Timeout check - avoid infinite loop
            if time.time() - start_time > SERVER_LOOKUP_TIMEOUT:
                return ""

        chosen = self.servers[self.pointer]
        self.pointer = (self.pointer + 1) % self.servers_lenght
        return chosen.endpoint


    @staticmethod
    def is_server_up(server: Server):
        try:
            response = requests.get(server.endpoint, timeout=5)
            server.is_healthy = response.status_code == 200
        except requests.exceptions.RequestException:
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
