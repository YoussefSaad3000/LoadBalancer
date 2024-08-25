class Server:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.is_healthy = False

    @staticmethod
    def get_servers_from_endpoints(endpoints):
        return list(Server(endpoint) for endpoint in endpoints)

    def __str__(self):
        return f"endpoint: {self.endpoint}, is_health: {self.is_healthy}"
