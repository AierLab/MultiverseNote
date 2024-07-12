# The main entry point for the backend server, responsible for initializing and running the web server.

from server import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)