import logging

from src.constants import LB_LOGGER
from src.logger_config import setup_logging
from src.load_balancer import LoadBalancer, Server
from flask import Flask
import requests


# Set up logging
setup_logging()
logger = logging.getLogger(LB_LOGGER)

app = Flask(__name__)


@app.route('/')
def home():
    global lb
    server = lb.get_next_server()
    if not server:
        return "No available server at this time "
    logger.info(f"the load balancer serve request to {server}")
    try:
        response = requests.get(server)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve the HTML file. Status code: {response.status_code}"
    except Exception as e:
        return f"Exception occurred while fetching the server {e}"


if __name__ == '__main__':
    servers = Server.get_servers_from_endpoints(
        ["http://localhost:8080", "http://localhost:8081", "http://localhost:8082"])
    lb = LoadBalancer(servers)

    app.run(host='0.0.0.0', port=80)
