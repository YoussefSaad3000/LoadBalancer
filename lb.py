from src.load_balancer import LoadBalancer, Server
from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def home():
    server = lb.get_next_server()
    print(f"the load balancer serve request from {server}")
    try:
        response = requests.get(server)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve the HTML file. Status code: {response.status_code}"
    except Exception as e:
        return f"Exception occurred while fetching the server {e}"


if __name__ == '__main__':
    # Use host='0.0.0.0' to make the server publicly accessible
    servers = Server.get_servers_from_endpoints(["http://localhost:8080", "http://localhost:8081", "http://localhost:8082"])
    lb = LoadBalancer(servers)
    app.run(host='0.0.0.0', port=80)
