import click
import os
import xarray as xarray

@click.group()
@click.option("-f", "--folder", type=click.Path(exists=True), default=os.path.abspath("."))
@click.pass_context
def pytiles(ctx, folder):
    ctx.ensure_object(dict)
    ctx.obj["folder"]=os.path.abspath(folder)

@pytiles.command()
@click.pass_context
@click.option("-l","--layers")
@click.option("-s","--styles")
@click.option("--srs", default="EPSG:4236")
@click.option("-b","--bbox")
@click.option("-w","--width", type=click.INT)
@click.option("-h","--height", type=click.INT)
@click.option("-f","--format", "_format", default="img/png")
def getmap(ctx, layers, styles, srs, bbox, width, height, _format, **kwargs):
    from getmap import getmap
    getmap(ctx.obj["folder"], layers, styles, srs, bbox, width, height, _format, **kwargs)


if __name__ == "__main__":
    pytiles()