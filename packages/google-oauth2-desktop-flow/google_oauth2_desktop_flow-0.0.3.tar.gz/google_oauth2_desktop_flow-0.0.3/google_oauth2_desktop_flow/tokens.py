
import os
import webbrowser
import google_auth_oauthlib
from flask import Flask, request
from multiprocessing import Process, Queue

DEFAULT_CLIENT_SECRET_PATH = os.path.expanduser('~/.goauth/oauth_client_secret.json')


def get_tokens(scopes, client_secret_path=DEFAULT_CLIENT_SECRET_PATH):
    queue = Queue()
    app = Flask(__name__)

    @app.route('/')
    def get_oauth_code():
        code = request.args.get("code")
        queue.put(code)
        return 'You can close this window now!', 200

    server = Process(target=app.run, kwargs={'port': 8081})
    server.start()

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_path,
        scopes=scopes)
    flow.redirect_uri = 'http://127.0.0.1:8081'
    url = flow.authorization_url(access_type='offline')

    webbrowser.open(url[0])
    oauth_code = queue.get()
    server.terminate()
    flow.fetch_token(code=oauth_code)
    return flow.credentials
