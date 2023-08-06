#! /usr/bin/env python

import json

from beautifultable import BeautifulTable
from requests import Response, Session
import click


class CeryxClient:
    def __init__(self, base_url: str):
        self.session = Session()
        self.base_url = base_url
        self.api_root = f"{self.base_url}/api"

    def _get_route_url(self, host):
        return f"{self.api_root}/routes/{host}/"

    def _get_payload_from_kwargs(
        self, host, target, enforce_https, mode, certificate_path, key_path
    ):
        payload = {
            "source": host,
            "target": target,
            "settings": {
                "enforce_https": enforce_https,
                "mode": mode,
                "certificate_path": certificate_path,
                "key_path": key_path,
            },
        }
        return payload

    def _request(self, method, url, payload={}):
        kwargs = {} if method == "get" else {"json": payload}
        response: Response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def list_routes(self):
        return self._request("get", f"{self.api_root}/routes/").json()

    def get_route(self, host: str):
        route_url = self._get_route_url(host)
        return self._request("get", route_url).json()

    def delete_route(self, host: str):
        route_url = self._get_route_url(host)
        self._request("delete", route_url)
        return None

    def create_route(
        self,
        host,
        target,
        enforce_https=False,
        mode="proxy",
        certificate_path=None,
        key_path=None,
    ):
        payload = self._get_payload_from_kwargs(
            host=host,
            target=target,
            enforce_https=enforce_https,
            mode=mode,
            certificate_path=certificate_path,
            key_path=key_path,
        )
        response = self._request("post", f"{self.api_root}/routes/", payload)
        return response.json()

    def update_route(
        self,
        host,
        target,
        enforce_https=False,
        mode="proxy",
        certificate_path=None,
        key_path=None,
    ):
        payload = self._get_payload_from_kwargs(
            host=host,
            target=target,
            enforce_https=False,
            mode="proxy",
            certificate_path=None,
            key_path=None,
        )
        route_url = self._get_route_url(host)
        return self._request("put", route_url, payload).json()


# Set up CLI
@click.group()
@click.option(
    "--base-url",
    help="The base URL of your Ceryx API installation. Example: http://ceryx-api:5555.",
)
@click.pass_context
def cli(ctx, base_url):
    """Control Ceryx via the command line"""
    ctx.ensure_object(dict)
    ctx.obj["client"] = CeryxClient(base_url=base_url)
    pass


@cli.group()
def route():
    """Manage routes"""
    pass


@route.command()
@click.option(
    "--mode",
    type=click.Choice(["proxy", "redirect"]),
    default="proxy",
    show_default=True,
    help="Route requests via proxying or redirecting.",
)
@click.option(
    "--enforce-https",
    is_flag=True,
    show_default=True,
    help="Enforce HTTPS by redirecting HTTP requests to HTTPS.",
)
@click.option(
    "--key-path",
    default=None,
    type=click.Path(),
    show_default=True,
    help="Set a custom SSL key for HTTPS.",
)
@click.option(
    "--certificate-path",
    default=None,
    type=click.Path(),
    show_default=True,
    help="Set a custom certificate key for HTTPS.",
)
@click.argument("host")
@click.argument("target")
@click.pass_context
def create(ctx, host, target, mode, enforce_https, key_path, certificate_path):
    """Create a new route"""
    client = ctx.obj["client"]
    route = client.create_route(
        host=host,
        target=target,
        mode=mode,
        enforce_https=enforce_https,
        key_path=key_path,
        certificate_path=certificate_path,
    )
    formatted_json = json.dumps(route, indent=2)
    click.echo(formatted_json)


@route.command()
@click.pass_context
def ls(ctx):
    """List all routes"""
    client = ctx.obj["client"]
    routes = client.list_routes()

    # Output
    table = BeautifulTable(max_width=560)
    table.column_headers = ["Host", "Target", "Mode", "Enforce HTTPS"]

    table.set_style(BeautifulTable.STYLE_NONE)

    for column in table.column_headers:
        table.column_alignments[column] = BeautifulTable.ALIGN_LEFT
        table.left_padding_widths[column] = 0
        table.right_padding_widths[column] = 4

    for route in routes:
        row = [
            route["source"],
            route["target"],
            route["settings"]["mode"],
            route["settings"]["enforce_https"],
        ]
        table.append_row(row)

    click.echo(table)


@route.command()
@click.argument("host")
@click.pass_context
def inspect(ctx, host):
    """Inspect a route"""
    client = ctx.obj["client"]
    route = client.get_route(host=host)
    formatted_json = json.dumps(route, indent=2)
    click.echo(formatted_json)


@route.command()
def update():
    """Update a route"""


@route.command()
@click.argument("host")
@click.pass_context
def rm(ctx, host):
    """Remove a route"""
    client = ctx.obj["client"]
    client.delete_route(host=host)


if __name__ == "__main__":
    cli(auto_envvar_prefix="CERYX")
