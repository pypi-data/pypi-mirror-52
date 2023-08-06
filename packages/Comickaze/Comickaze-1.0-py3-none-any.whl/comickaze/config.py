from . import util
from os import path
import click
import json

FOLDER_NAME = "comickaze"
HOME = util.userFolder() + path.sep + FOLDER_NAME
DEFAULT_DL_PATH = HOME + path.sep + "downloads"
CONFIG_PATH = HOME + path.sep + "config.json"


def createComikazeFolder():
    util.createFolder(HOME)

def createConfig():
    click.echo("Comickaze Config Generator")
    downloadPath = click.prompt("Download directory", default=DEFAULT_DL_PATH, type=click.Path())

    createComikazeFolder()

    data = {
        "downloadDir": downloadPath
    }

    save(data)

def save(data):
    with open(path.normpath(CONFIG_PATH), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read():
    with open(path.normpath(CONFIG_PATH), "r", encoding="utf-8") as f:
        return json.load(f)

def getDLPath():
	try:
		conf = read()
		if "downloadDir" in conf:
			return conf["downloadDir"]
		else:
			raise
	except FileNotFoundError as fileNotFound:
		return path.normpath(DEFAULT_DL_PATH)