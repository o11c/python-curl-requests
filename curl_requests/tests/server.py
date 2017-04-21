import httpbin
from werkzeug.serving import BaseWSGIServer


def start_app(app, ssl):
    server = BaseWSGIServer(host='localhost', port=0, app=app)
    server.my_extra = None
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

http_port = start_app(httpbin.app, False).server_port
