
import os
import webbrowser
import google_auth_oauthlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from multiprocessing import Process, Queue

DEFAULT_CLIENT_SECRET_PATH = os.path.expanduser('~/.goauth/oauth_client_secret.json')

Q = Queue()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_query = parse_qs(urlparse(self.path).query)

        if not parsed_query:
            raise ValueError("Received empty URL query string.")

        code = parsed_query.get('code', None)
        if not code:
            raise ValueError("OAuth code not found in query string.")

        Q.put(parsed_query['code'][0])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'You can close this window now!')
        self.server.shutdown()


def get_tokens(scopes, client_secret_path=DEFAULT_CLIENT_SECRET_PATH):
    server = HTTPServer(('127.0.0.1', 8081), RequestHandler)
    server = Process(target=server.serve_forever)
    server.start()

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_path,
        scopes=scopes)
    flow.redirect_uri = 'http://127.0.0.1:8081'
    url = flow.authorization_url(access_type='offline')

    webbrowser.open(url[0])
    print('Open the following URL in the browser:', url[0])
    oauth_code = Q.get()
    server.terminate()
    flow.fetch_token(code=oauth_code)
    return flow.credentials
