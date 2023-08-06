from . import util
from os import path
import click
import json

FOLDER_NAME = "comickaze"
HOME = path.join(util.userFolder(), FOLDER_NAME)
DEFAULT_DL_PATH = path.join(HOME, "downloads") 
DEFAULT_OUTPUT_FORMAT = "cbz"
CONFIG_PATH = path.join(HOME, "config.json")


def createComikazeFolder():
    util.createFolder(HOME)

def createConfig():
    click.echo("Comickaze Config Generator")
    downloadPath = click.prompt("Download directory", default=DEFAULT_DL_PATH, type=click.Path())
    outFormat = click.prompt("Output format", default=DEFAULT_OUTPUT_FORMAT, type=click.Choice(["cbz", "pdf", "jpg"], case_sensitive=False))

    createComikazeFolder()

    data = {
        "downloadDir": downloadPath,
        "outputFormat": outFormat.lower()
    }

    save(data)

    click.echo("Configuration successfully created!")

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
	except Exception:
		return path.normpath(DEFAULT_DL_PATH)

def getOutputFormat():
    try:
        conf = read()
        if "outputFormat" in conf:
            return conf["outputFormat"]
        else:
            raise
    except Exception:
        return DEFAULT_OUTPUT_FORMAT 