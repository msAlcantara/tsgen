import sys
import click
import pandas as pd
import numpy as np
from pytz.exceptions import UnknownTimeZoneError
from os import path
from .gen import TimeSerieGenerator


def version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        version_file = path.join(path.abspath(path.dirname(__file__)), "VERSION")
        with open(version_file) as f:
            click.echo(f"v{f.read().strip()}")
    except FileNotFoundError:
        click.echo(
            "error: tsgen not installed correctly\n Try running python setup.py install"
        )
    ctx.exit()


@click.command()
@click.option(
    "-s",
    "--date-start",
    required=True,
    type=pd.Timestamp,
    help="Date start of timeseries data [YYYY-MM-DD]/[YYYY-MM-DD HH:MM:SS]",
)
@click.option(
    "-e",
    "--date-end",
    default=None,
    type=pd.Timestamp,
    help="Date end of timeseries data [YYYY-MM-DD]/[YYYY-MM-DD HH:MM:SS]  [default: now]",
)
@click.option(
    "-f",
    "--freq", default="D", show_default=True, help="Frequency of dates, e.g. '5H'"
)
@click.option(
    "--tz", type=str, default="UTC", show_default=True, help="Timezone of dates"
)
@click.option("--low", default=0, show_default=True, help="Lowest data to be generated")
@click.option(
    "--high", default=None, required=True, help="Largest data to be generated"
)
@click.option(
    "--version", is_flag=True, callback=version, expose_value=False, is_eager=True
)
@click.argument("timeserie-name", required=True)
def main(date_end, **kwargs):
    try:
        if date_end is None:
            date_end = pd.Timestamp.now(tz=kwargs["tz"])
        TimeSerieGenerator(
            kwargs["date_start"],
            date_end,
            kwargs["freq"],
            kwargs["tz"],
            kwargs["low"],
            kwargs["high"],
            kwargs["timeserie_name"],
        ).generate()
    except UnknownTimeZoneError as e:
        print(f"Unknown TimeZone Error: {e}")


if __name__ == "__main__":
    main()
