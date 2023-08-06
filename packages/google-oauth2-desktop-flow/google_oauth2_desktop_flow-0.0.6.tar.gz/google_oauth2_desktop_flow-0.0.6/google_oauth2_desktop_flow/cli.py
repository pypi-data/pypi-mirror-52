import os
import click
from google_oauth2_desktop_flow.tokens import get_tokens

DEFAULT_CLIENT_SECRET_PATH = os.path.expanduser('~/.goauth/oauth_client_secret.json')


@click.command()
@click.option('-s', '--scopes', required=True, multiple=True, type=str)
@click.option('-c', '--client-secret-path', default=DEFAULT_CLIENT_SECRET_PATH)
def main(scopes, client_secret_path):
    credentials = get_tokens(scopes, client_secret_path)
    click.secho('Google OAuth2.0 Tokens', fg='green', bold=True, underline=True)

    click.secho('Access Token: ', fg='green', nl=False)
    click.echo(credentials.token)
    click.secho('Refresh Token: ', fg='green', nl=False)
    click.echo(credentials.refresh_token)
    click.secho('Token Uri: ', fg='green', nl=False)
    click.echo(credentials.token_uri)
    click.secho('Client Id: ', fg='green', nl=False)
    click.echo(credentials.client_id)
    click.secho('Scopes: ', fg='green', nl=False)
    click.echo(', '.join(credentials.scopes))
