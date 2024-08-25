import threading
from src.load_balancer import LoadBalancer, Server
from flask import Flask
import requests

app = Flask(__name__)
lb = None
# event = threading.Event()

@app.route('/')
def home():
    global lb
    print("hna f home:", lb)
    print("event 9bal wait : ",event)
    # event.wait()
    print("event after wait: ",event)
    server = lb.get_next_server()
    if not server:
        return "No available server at this time "
    print(f"the load balancer serve request from {server}")
    try:
        response = requests.get(server)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve the HTML file. Status code: {response.status_code}"
    except Exception as e:
        return f"Exception occurred while fetching the server {e}"

# def run_load_balancer():
#     global lb
#     print("run_load_balancer lb 1 ", lb)
#     # servers = Server.get_servers_from_endpoints(["http://localhost:8080", "http://localhost:8081", "http://localhost:8082"])
#     # lb = LoadBalancer(servers)
#     lb.health_check_ticker()
#     print("run_load_balancer lb 2 ", lb)
#     # # event.set()
#     # print("event: ",event)



if __name__ == '__main__':
    # Use host='0.0.0.0' to make the server publicly accessible
    servers = Server.get_servers_from_endpoints(["http://localhost:8080", "http://localhost:8081", "http://localhost:8082"])
    lb = LoadBalancer(servers)
    print("lb in main 1")
    # lb_thread = threading.Thread(target=run_load_balancer)

    # lb_thread.daemon = True  
    # lb_thread.start()

    
    print("lb in main 2  ", lb)
    
    app.run(host='0.0.0.0', port=80)


   
