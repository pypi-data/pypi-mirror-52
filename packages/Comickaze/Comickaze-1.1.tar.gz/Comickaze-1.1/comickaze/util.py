from bs4 import BeautifulSoup
from tabulate import tabulate
import click
import os
from os import path
import sys
import requests
import shutil

def createSession():
    return requests.Session()

def soupify(data):
    return BeautifulSoup(data, "html.parser")

def userFolder():
    return path.expanduser("~")

def createFolder(target_path):
    try:
        if not path.exists(target_path):
            os.makedirs(path.normpath(target_path))
    except OSError as e:
        click.echo("Error creating directory: " + target_path, err=True)
        click.echo("Error: " + repr(e), err=True)
        sys.exit()

def deleteFolder(target_path):
    try:
        if path.exists(target_path):
            shutil.rmtree(target_path)
    except OSError as e:
        click.echo("Error deleting directory: " + target_path,  err=True)
        click.echo("Error: " + repr(e), err=True)
        sys.exit()