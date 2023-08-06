#!/usr/bin/env python
# encoding: utf-8

import click
from pathlib import Path
import yaml
import sys
import papermill as pm
from datetime import datetime

CONFIGPATH = "recoconfig.yml"

with open(CONFIGPATH, "r") as config:
    config = yaml.load(config, Loader=yaml.FullLoader)


@click.group()
def cli():
    pass


@cli.command()
def print_config():
    click.echo(f"Config file is {CONFIGPATH}")
    click.echo("It contains")
    click.echo(config)


@cli.command()
@click.argument("csv_file")
def report(csv_file):
    csv = Path(csv_file)
    if not csv.exists():
        click.echo(f"{csv_file} does not exists")
        sys.exit(1)
    if csv.suffix != ".csv":
        click.echo(f"{csv_file} has to be a csv file")
        sys.exit(1)

    csv_file = Path(csv_file)
    tribe_dir = csv_file.parent
    csv_filename = csv_file.name.split(".")[0]

    assessment = str(csv_filename).split("_")[-1].capitalize()
    date = str(csv_filename).split("_")[0]
    try:
        date = datetime.strptime(date, "%y%m%d")
    except ValueError:
        date = None

    tribe = str(tribe_dir).split("/")[-1]

    template = Path(config["templates"]) / "tpl_evaluation.ipynb"

    dest = Path(config["output"]) / tribe / csv_filename
    dest.mkdir(parents=True, exist_ok=True)

    click.echo(f"Building {assessment} ({date:%d/%m/%y}) report")
    pm.execute_notebook(
        str(template),
        str(dest / f"{assessment}.ipynb"),
        parameters=dict(
            tribe=tribe, assessment=assessment, date=f"{date:%d/%m/%y}", csv_file=str(csv_file.absolute())
        ),
    )

    # with open(csv_file.parent / "description.yml") as f:
    #     tribe_desc = yaml.load(f, Loader=yaml.FullLoader)

    # template = Path(config["templates"]) / "tpl_student.ipynb"
    # dest = Path(config["output"]) / tribe / csv_filename / "students"
    # dest.mkdir(parents=True, exist_ok=True)

    # for st in tribe_desc["students"]:
    #     click.echo(f"Building {st} report on {assessment}")
    #     pm.execute_notebook(
    #         str(template),
    #         str(dest / f"{st}.ipynb"),
    #         parameters=dict(tribe=tribe, student=st, source=str(tribe_dir.absolute())),
    #     )

