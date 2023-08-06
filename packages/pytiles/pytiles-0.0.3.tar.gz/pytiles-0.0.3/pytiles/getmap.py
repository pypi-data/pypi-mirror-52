import os   
import glob
import numpy as np
import rasterio
from rasterio.warp import reproject
import matplotlib.pyplot as plt
import png
import base64
from io import BytesIO
from matplotlib import cm
from PIL import Image
def getmap(folder, layers, bbox, width, height, _format="image/png", styles="", srs="EPSG:4326", **kwargs):
    ls = glob.glob(os.path.join(folder, layers+".*"))
    if not ls:
        raise RuntimeError("No layer named %s" % layers)

    srs = srs.split(":")[-1]

    out = np.zeros((int(height), int(width)))
    bbox = list(map(float, bbox.split(",")))

    dx = (bbox[2]-bbox[0])/int(width)
    dy = (bbox[3] - bbox[1])/int(height)

    transform = rasterio.Affine(dx, 0, bbox[0], 0, -dy, bbox[3])
    crs = rasterio.crs.CRS.from_epsg(srs)

    ds = rasterio.open(ls[0])
    src_transform=ds.transform
    src_crs=ds.crs

    reproject(
        ds.read(1),
        out,
        src_crs=ds.crs,
        src_nodata=ds.nodata,
        src_transform=ds.transform,
        dst_crs=crs,
        dst_transform=transform,
        dst_nodata=-9999
        )
    
    buffered = BytesIO()
    RGBA  = np.uint8(cm.gist_earth(out/300)*255)

    mBlack = np.isnan(out)
    RGBA[mBlack] = (0,0,0,0)
    im  = Image.fromarray(RGBA)
    im.save(buffered, format="PNG")

    return buffered.getvalue()