import click
import os

@click.group()
@click.option("-f", "--folder", type=click.Path(exists=True), default=os.path.abspath("."))
@click.pass_context
def pytiles(ctx, folder):
    """pyTiles: OGC WMS server implementation in python
    
    Arguments:
        ctx {[type]} -- [description]
        folder {[type]} -- [description]
    """
    ctx.ensure_object(dict)
    ctx.obj["folder"]=os.path.abspath(folder)

@pytiles.command()
def getCapabilities():
    """Get capabilities of the pytiles server
    """
    pass

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
    """GetMap request for wms
    
    Arguments:
        ctx {[type]} -- [description]
        layers {[type]} -- [description]
        styles {[type]} -- [description]
        srs {[type]} -- [description]
        bbox {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
        _format {[type]} -- [description]
    """
    from getmap import getmap
    getmap(ctx.obj["folder"], layers, styles, srs, bbox, width, height, _format, **kwargs)

@pytiles.command()
def getFeatureInfo():
    """Get feature information for a specific location
    """
    pass


@pytiles.command()
def getLegend():
    """Get legend of a specific pytiles layer
    """
    pass

@pytiles.command()
@click.pass_context
def serve(ctx):
    """Launches a pytiles server that can be used in a web mapping application
    """
    from .server import getapp
    app = getapp(ctx.obj["folder"])
    app.run()

if __name__ == "__main__":
    pytiles()