import click

from ..classes import Config
from ..classes import Json


@click.command("json", help="Build the json files for your gallery.")
@click.option("--albums", help="Only export the json files for the albums view.", is_flag=True)
@click.option("--timeline", help="Only export the json files for the timeline view.", is_flag=True)
@click.option(
    "--output-dir",
    "-o",
    help="Set a different output dir. This will overrule the " "json_data_dir setting of your config file.",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True),
)
@click.argument("config-file", required=False, type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def jsongen(config_file, output_dir=None, albums=False, timeline=False, *args, **kwargs):
    json = Json(Config(config_file), output_dir=output_dir)
    if not albums and not timeline:
        albums, timeline = True, True
    json.generate(albums=albums, timeline=timeline)
