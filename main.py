import socket
from _init_ import create_app

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = create_app()

if __name__ == '__main__':
    
    app.run(host=IPAddr, port = 8080 ,debug=True, threaded=True, use_reloader=False)

