#!/usr/bin/env python3

"""Find an instance's place in the Mastodon rankings.

This fetches the quasi-official list of Mastodon instances, sorts them by each column, and reports
the given instance's ranking within that column.

©2017, 2018 Kirk Strauser <kirk@strauser.com>. GPL license v3 or newer.
"""

import json
import logging
import pathlib
import time
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Tuple, Union

import click
import requests
from bs4 import BeautifulSoup  # type: ignore

Columns = List[str]  # pylint: disable=invalid-name
Row = Dict[str, Any]  # pylint: disable=invalid-name

INSTANCES_URL = "https://instances.social/list/old"

COL_CONNECTIONS = "Connections"
COL_HTTPS = "HTTPS"
COL_INSTANCE = "Instance"
COL_IPV6 = "IPv6"
COL_OBS = "Obs"
COL_PERUSER = "PerUser"
COL_REGISTRATIONS = "Registrations"
COL_SCORE = "Score"
COL_STATUSES = "Statuses"
COL_UP = "Up"
COL_UPTIME = "Uptime"
COL_USERS = "Users"

SKIP_COLS = {COL_HTTPS, COL_INSTANCE, COL_IPV6, COL_OBS}

LOG = logging.getLogger(__name__)
SMALL_NUM = float("-inf")


def cacher(cache_name: str = None, duration: int = 300) -> Callable:
    """Cache the results of a function call for a period of time."""

    def outer(func: Callable) -> Callable:
        """Return a decorator that caches the function call."""

        nonlocal cache_name

        if cache_name is None:
            cache_name = f"/tmp/{func.__name__}.cache"

        @wraps(func)
        def inner(*args, **kwargs):
            """Call a function, or possibly return its cached results."""

            cache = pathlib.Path(cache_name)
            if cache.exists() and time.time() < cache.stat().st_mtime + duration:
                LOG.info("Using cache %s", cache_name)
                with cache.open() as infile:
                    return json.load(infile)

            data = func(*args, **kwargs)

            with cache.open("w") as outfile:
                LOG.info("Saving cache %s", cache_name)
                json.dump(data, outfile)

            return data

        return inner

    return outer


@cacher()
def get_data(url: int) -> Tuple[Columns, List[Row]]:
    """Return a list of column names and a list of row dicts from the parsed page."""

    soup = BeautifulSoup(get_page(url), "lxml")
    table = soup.find("table", class_="table-sm")
    columns = get_columns(table)
    rows = list(get_rows(table, columns))

    return columns, rows


@cacher()
def get_page(url: str) -> str:
    """Return the instance list page's text contents."""

    return requests.get(url).text


def get_columns(table: BeautifulSoup) -> Columns:
    """Return the list of column names from the instance list."""

    columns = [th.text for th in table.find("tr").find_all("th")]
    columns[0] = COL_UP
    return columns


def get_rows(table: BeautifulSoup, columns: List[str]) -> Generator[Row, None, None]:
    """Yield a series of dicts representing HTML table rows."""

    rows = table.find_all("tr")

    bool_up = "UP"
    bool_yes = "Yes"

    for row in rows[1:]:
        values = [_.text.strip() for _ in row.find_all("td")]

        row = dict(zip(columns, values))

        users = row[COL_USERS] = intish(row[COL_USERS])
        row[COL_CONNECTIONS] = intish(row[COL_CONNECTIONS])
        row[COL_IPV6] = row[COL_IPV6] == bool_yes
        row[COL_REGISTRATIONS] = row[COL_REGISTRATIONS] == bool_yes
        row[COL_SCORE] = float(row[COL_SCORE])
        row[COL_STATUSES] = intish(row[COL_STATUSES])
        row[COL_UPTIME] = float(row[COL_UPTIME].rstrip("%"))
        row[COL_UP] = row[COL_UP] == bool_up
        row[COL_PERUSER] = row[COL_STATUSES] / users if users else SMALL_NUM

        yield row


def intish(value: str) -> Union[int, float]:
    """Cast an intlike value to an int."""

    return SMALL_NUM if value == "" or value is SMALL_NUM else int(value)


def sort_key(key: str, instance: str) -> Callable[[Any], Tuple[Any, bool]]:
    """Return a sorting function on the key.

    In event of a tie, the search instance is sorted to the bottom of
    the list (after reversing). For example, if 100 instances have
    value "True" and 100 have "False", and the search instance is
    True, then we want it to show the 50th percentile, not some random
    ranking in the top 50%.
    """

    def inner(value: Row):
        """Like a context-aware itemgetter."""

        return (value[key], value[COL_INSTANCE] != instance)

    return inner


@click.command()
@click.argument("instance_name")
def report_instance(instance_name):
    """Display the report for the given instance name."""

    columns, rows = get_data(INSTANCES_URL)

    count = len(rows)
    print(
        f"""\
Instances: {count}

{"Column":<14}  {"Value":7}  {"Rank":>5}  {"Pctl"}
------------------------------------"""
    )

    for column in sorted(columns + [COL_PERUSER]):
        if column in SKIP_COLS:
            continue

        rows.sort(key=sort_key(column, instance_name), reverse=True)

        instances = [row[COL_INSTANCE] for row in rows]

        index = instances.index(instance_name)
        row = rows[index]

        rank = index + 1
        value = str(row[column])[:7]
        percent = (1 - (rank / count)) * 100
        print(f"{column:<14}  {value:7}  {rank:>5}  {percent:>4.1f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    report_instance()  # pylint: disable=no-value-for-parameter
