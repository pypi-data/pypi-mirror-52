import click

from ..classes import Config
from ..classes import Index


@click.command("index", help="Index all photos in your source directory")
@click.option(
    "--index-dir",
    "-i",
    help="Specify directory where your original photos are. Can be set " "multiple times.",
    multiple=True,
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
)
@click.option(
    "--update-album-meta",
    "-u",
    help="Only check existing meta files and save changes. No photo or " "directory indexing.",
    is_flag=True,
)
@click.option("--image-meta", "-m", help="Reprocess all image meta data.", is_flag=True)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def index(config_file, index_dir=[], image_meta=False, update_album_meta=False, *args, **kwargs):
    index = Index(Config(config_file))
    if update_album_meta:
        index.update_album_meta()
    else:
        index.index(dirs=index_dir, reprocess_image_meta=image_meta)
