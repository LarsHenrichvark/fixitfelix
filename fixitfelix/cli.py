import click
import pathlib
import yaml

from typing import Optional

from fixitfelix import config, fix, source


PATH_TO_CONFIG = pathlib.Path.home().joinpath(".fixitfelix_config.yaml")
CLI_CONFIG = config.CliConfig.from_yaml(PATH_TO_CONFIG)


@click.command()
@click.argument(
    "filename", type=click.Path(file_okay=True, dir_okay=True, exists=True)
)
@click.option(
    "--recurrence_size",
    prompt=True,
    default=CLI_CONFIG.recurrence_size,
    type=int,
    help="Length of a bad data chunk, copied from a position before",
)
@click.option(
    "--recurrence_distance",
    prompt=True,
    default=CLI_CONFIG.recurrence_distance,
    type=int,
    help="Distance from the bad data to the position they are taken from",
)
@click.option(
    "--chunk_size",
    prompt=True,
    default=CLI_CONFIG.chunk_size,
    type=int,
    help="Length of a chunk of good data, each written to disk one after another",
)
@click.option(
    "-c",
    "--consistency_sample_size",
    prompt=True,
    default=CLI_CONFIG.consistency_sample_size,
    type=int,
    help="Number of random samples in which the consistency of the TdmsFile and the given meta data is checked",
)
@click.option("-o", "--output_file", default="")
@click.option(
    "-m",
    "--usable_memory",
    prompt=True,
    default=CLI_CONFIG.usable_memory,
    type=int,
    help="Amount of memory (in gigabyte) available to read and write channels ",
)
def main(
    recurrence_size: int,
    recurrence_distance: int,
    chunk_size: int,
    consistency_sample_size: int,
    output_file: str,
    filename: str,
    usable_memory: int,
):
    meta = source.MetaData(
        recurrence_distance=recurrence_distance,
        recurrence_size=recurrence_size,
        chunk_size=chunk_size,
        consistency_sample_size=consistency_sample_size,
        usable_memory=usable_memory,
    )

    fix.export_correct_data(
        filename=filename, meta=meta, output_file=output_file
    )

    CLI_CONFIG.update_config(
        recurrence_distance=recurrence_distance,
        recurrence_size=recurrence_size,
        chunk_size=chunk_size,
        consistency_sample_size=consistency_sample_size,
        usable_memory=usable_memory,
    )
    CLI_CONFIG.to_yaml(PATH_TO_CONFIG)
