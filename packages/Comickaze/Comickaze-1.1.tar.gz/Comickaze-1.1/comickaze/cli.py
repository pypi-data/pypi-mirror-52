import click
import sys
from . import config as conf, util
from .Comickaze import Comickaze, COMIC_URL

@click.group()
def cli():
    """A CLI tool to download comics"""
    pass

@cli.command()
@click.option("--path", default=conf.getDLPath(), show_default=False, help="Specifies the download directory", type=click.Path())
@click.option("--dl-range", "--range", default="*", help="Specifies the range of issues to be downloaded, Ex: 1-5 or 1-*. See docs for valid inputs.", show_default=True, type=click.STRING)
@click.option("--output-format", "--format", default=conf.getOutputFormat(), help="Specifies the output format of the download comics", type=click.Choice(["cbz", "pdf", "jpg"], case_sensitive=False))
@click.argument("comic")
def dl(comic, dl_range, path, output_format):
    """Comickaze : Downloader"""
    try:
        if dl_range != "*":
            dl_range = dl_range.split("-")

            startTest = dl_range[0]
            if startTest == "*":
                raise
            startTest = int(startTest)

            endTest = dl_range[1]
            if endTest != "*":
                endTest = int(endTest)
    except Exception:
        click.echo("The given path is invalid. The valid format is: <start>-<end> or <start>-*")
        sys.exit()
    
    comickaze = Comickaze()
    res = comickaze.search(comic)

    if res:
        click.echo("Search results for {0}.".format(comic))
        tableHeaders = [
            "Comic ID",
            "Comic"
        ]
        content = [(i + 1, comic["title"]) for i, comic in enumerate(res)]
        table = util.tabulate(content, headers=tableHeaders, tablefmt="psql")
        click.echo(table)
        cid = click.prompt("Input the Comic ID of desired Comic", type=click.IntRange(1, len(res))) - 1

        comic = res[cid]

        downloader = comickaze.downloader(comic, path, dl_range=dl_range, output_format=output_format)
        downloader.startDownload()
    else:
        click.echo("No comics found with that given query, please choose a better term.")
    

@cli.command()
def config():
    """Comickaze : Configuration"""
    conf.createConfig()