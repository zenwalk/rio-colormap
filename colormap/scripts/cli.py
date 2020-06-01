"""Cowsay raster dataset metdata items"""

import sys

import click
import rasterio
import json
import os

from colormap import __version__ as colormap_version


@click.command(short_help="Cowsay some dataset metadata.")
@click.argument('inputfile', type=click.Path(resolve_path=True), required=True,
                metavar="INPUT")
@click.option('--band', default=1, help="Select a band.")
@click.option('--colormap', required=False)
@click.version_option(version=colormap_version, message='%(version)s')
@click.pass_context
def colormap(ctx, inputfile, band, colormap):
    """Moo some dataset metadata to stdout.

    Python module: rio-metasay
    (https://github.com/sgillies/rio-plugin-example).
    """
    mode = 'r'

    if os.path.exists(colormap):
        try:
            my_colormap = json.load(open(colormap))
            mode = 'r+'
        except Exception as e:
            click.echo(e)
            sys.exit()
    
    with rasterio.open(inputfile, mode=mode) as src:
        meta = src.profile
        if mode == 'r':
            try:
                d = src.colormap(band)
                ret = json.dumps(d)
                click.echo(ret)
            except Exception as e:
                click.echo(e)
        else:
            try:
                src.write_colormap(1, my_colormap)
            except Exception as e:
                click.echo(e)
