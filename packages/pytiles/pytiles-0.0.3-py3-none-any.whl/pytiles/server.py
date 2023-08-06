from flask import Flask, request, Response, make_response
from click.testing import CliRunner
from flask_caching import Cache

def getapp(folder):

    app = Flask(__name__)
    cache = Cache(app, config={"CACHE_TYPE": "simple"})

    @app.route("/wms")
    def wms():
        from .getmap import getmap
        data = request.args
        runner = CliRunner()
        
        output = getmap(folder=folder, **data)
        response = make_response(output)
        response.headers.set("Content-Type", "image/png")
        return response
    
    return app