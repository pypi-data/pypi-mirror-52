import click
import os
import sys
import textwrap
import getpass

from ..clients import Client
from .printers import jsonify, pythonify


@click.group()
def cloud():
    """
    Commands to interact with SoupStars cloud.
    """

    pass


@cloud.command()
def health():
    """
    Print the status of the SoupStars api
    """

    resp = Client().health()
    jsonify(resp.json())


@cloud.command()
def login():
    """
    Log in with an existing email
    """

    client = Client()
    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')

    resp = client.login(email=email, password=password)

    if resp.ok:
        client.token = resp.json()['token']
        client.config.save()

    jsonify(resp.json())


@cloud.command()
def ls():
    """
    Show the parsers uploaded to SoupStars cloud
    """

    client = Client()
    resp = client.ls()
    jsonify(resp.json())


@cloud.command()
def register():
    """
    Register a new account on SoupStars cloud
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    password2 = getpass.getpass(prompt='Confirm password: ')

    if password != password2:
        print("Passwords did not match.")
        return

    client = Client()
    resp = client.register(email=email, password=password)

    if resp.ok:
        client.token = resp.json()['token']
        client.config.save()

    jsonify(resp.json())


@cloud.command()
def whoami():
    """
    Print the email address of the current user
    """

    client = Client()
    resp = client.profile()
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True,
              help="Name of the parser to push")
def push(module):
    """
    Push a parser to SoupStars cloud
    """

    client = Client()
    resp = client.push(module)
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True,
              help="Name of the parser to pull")
def pull(module):
    """
    Pull a parser from SoupStars cloud into a local module
    """

    client = Client()
    resp = client.pull(module)
    data = resp.json()
    with open(data['parser']['name'], 'w') as o:
        o.write(data['module'])
    jsonify({"state": "done", "response": data})


@cloud.command()
@click.option('--module', '-m', required=True,
              help="Name of the parser to create")
@click.option('--async/--no-async', '_async', default=False,
              help="Run the parser asynchronously. Default false.")
def run(module, _async):
    """
    Run a parser on SoupStars cloud
    """

    client = Client()
    resp = client.run(module, _async=_async)
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True,
              help="Name of the parser to show")
@click.option('--json/--no-json', default=False,
              help="Show parser details in JSON")
def show(module, json):
    """
    Show the contents of a parser on SoupStars cloud
    """

    client = Client()
    resp = client.pull(module)

    if json:
        jsonify(resp.json())
    else:
        pythonify(resp.json()['module'])


@cloud.command()
@click.option('--module', '-m', required=True,
              help="Name of the parser to test")
def results(module):
    """
    Print results of a parser
    """

    client = Client()
    resp = client.results(module)
    jsonify(resp.json())
