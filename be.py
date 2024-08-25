import logging

from src.constants import LB_LOGGER
from src.logger_config import setup_logging
import subprocess
import time
import json


# Set up logging
setup_logging()
logger = logging.getLogger(LB_LOGGER)


def start_server(port):
    with open('config.json', 'r') as file:
        config = json.load(file)
    python_version = config["python_version"]
    # Start the HTTP server in the background
    return subprocess.Popen([python_version, '-m', 'http.server', str(port), '--directory', 'resources/server'+str(port)])


def main():
    # Start three servers
    processes = []
    for port in [8080, 8081, 8082]:
        logger.info(f"Starting server on port {port}...")
        proc = start_server(port)
        processes.append(proc)
        time.sleep(1)  # Give some time for the server to start

    # Wait for all servers to finish (they run indefinitely)
    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        logger.info("Stopping servers...")
        for proc in processes:
            proc.terminate()


if __name__ == "__main__":
    main()
