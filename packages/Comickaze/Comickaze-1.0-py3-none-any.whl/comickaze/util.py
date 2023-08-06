from bs4 import BeautifulSoup
from tabulate import tabulate
import click
import os
import sys
import requests

def createSession():
    return requests.Session()

def soupify(data):
    return BeautifulSoup(data, "html.parser")

def userFolder():
    return os.path.expanduser("~")

def createFolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(os.path.normpath(path))
    except OSError as e:
        click.echo("Error creating directory: " + path)
        click.echo("Error: " + repr(e))
        sys.exit()