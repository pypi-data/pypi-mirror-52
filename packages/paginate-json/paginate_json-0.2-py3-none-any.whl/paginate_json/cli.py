import click
import requests
import json

try:
    import pyjq
except ImportError:
    pyjq = None


@click.command()
@click.version_option()
@click.argument("url", type=str, required=True)
@click.option("--nl", help="Output newline-delimited JSON", is_flag=True)
@click.option("--jq", help="jq transformation to run on each page")
@click.option("--accept", help="Accept header to send")
def cli(url, nl, jq, accept):
    """
    Fetch paginated JSON from a URL
    """
    if jq and not pyjq:
        raise click.ClickException(
            "Missing dependency: 'pip install pyjq' for this to work"
        )

    if nl:
        for chunk in paginate(url, jq, accept):
            click.echo(len(chunk), err=True)
            for row in chunk:
                click.echo(json.dumps(row))
    else:
        all = []
        for chunk in paginate(url, jq):
            all.extend(chunk)
        click.echo(json.dumps(all, indent=2))


def paginate(url, jq, accept=None):
    while url:
        click.echo(url, err=True)
        headers = {}
        if accept is not None:
            headers["Accept"] = accept
        response = requests.get(url, headers=headers)
        try:
            url = response.links.get("next").get("url")
        except AttributeError:
            url = None
        if jq:
            yield pyjq.first(jq, response.json())
        else:
            yield response.json()
