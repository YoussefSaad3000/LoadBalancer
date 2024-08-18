from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def home():
    server8080 = "http://localhost:8084"
    try:
        response = requests.get(server8080)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve the HTML file. Status code: {response.status_code}"
    except Exception as e:
        return f"Exception occurred while fetching the server {e}"


if __name__ == '__main__':
    # Use host='0.0.0.0' to make the server publicly accessible
    app.run(host='0.0.0.0', port=80)
