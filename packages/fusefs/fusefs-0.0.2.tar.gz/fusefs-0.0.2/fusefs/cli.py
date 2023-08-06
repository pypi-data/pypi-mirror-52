# -*- coding: utf-8 -*-

"""Console script for fusefs."""
import sys
import click

from fusefs import mount_fs


@click.command()
@click.argument("url")
@click.argument("mountpoint")
@click.option("-d", "--debug", is_flag=True, default=False, help="Activate debug logs.")
def main(url, mountpoint, debug):
    """Mount a pyFilesystem resource URL to MOUNTPOINT."""
    mount_fs(mountpoint, url, debug=debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
