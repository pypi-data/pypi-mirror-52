"""
Functions about cleaning feeds.
"""
import math
from typing import TYPE_CHECKING

import pandas as pd
import numpy as np

from . import constants as cs

# Help mypy but avoid circular imports
if TYPE_CHECKING:
    from .feed import Feed


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip the whitespace from all column names in the given DataFrame
    and return the result.
    """
    f = df.copy()
    f.columns = [col.strip() for col in f.columns]
    return f


def clean_ids(feed: "Feed") -> "Feed":
    """
    In the given Feed, strip whitespace from all string IDs and
    then replace every remaining whitespace chunk with an underscore.
    Return the resulting Feed.
    """
    # Alter feed inputs only, and build a new feed from them.
    # The derived feed attributes, such as feed.trips_i,
    # will be automatically handled when creating the new feed.
    feed = feed.copy()

    for table in cs.GTFS_REF["table"].unique():
        f = getattr(feed, table)
        if f is None:
            continue
        for column in cs.GTFS_REF.loc[cs.GTFS_REF["table"] == table, "column"]:
            if column in f.columns and column.endswith("_id"):
                try:
                    f[column] = f[column].str.strip().str.replace(r"\s+", "_")
                    setattr(feed, table, f)
                except AttributeError:
                    # Column is not of string type
                    continue

    return feed


def clean_times(feed: "Feed") -> "Feed":
    """
    In the given Feed, convert H:MM:SS time strings to HH:MM:SS time
    strings to make sorting by time work as expected.
    Return the resulting Feed.
    """

    def reformat(t):
        if pd.isna(t):
            return t
        t = t.strip()
        if len(t) == 7:
            t = "0" + t
        return t

    feed = feed.copy()
    tables_and_columns = [
        ("stop_times", ["arrival_time", "departure_time"]),
        ("frequencies", ["start_time", "end_time"]),
    ]
    for table, columns in tables_and_columns:
        f = getattr(feed, table)
        if f is not None:
            f[columns] = f[columns].applymap(reformat)
        setattr(feed, table, f)

    return feed


def drop_zombies(feed: "Feed") -> "Feed":
    """
    In the given Feed, do the following in order and return the resulting Feed.

    1. Drop stops of location type 0 or NaN with no stop times.
    2. Remove undefined parent stations from the ``parent_station`` column.
    3. Drop trips with no stop times.
    4. Drop shapes with no trips.
    5. Drop routes with no trips.
    6. Drop services with no trips.

    """
    feed = feed.copy()

    f = feed.stops.copy()
    ids = feed.stop_times.stop_id.unique()
    cond = f.stop_id.isin(ids)
    if "location_type" in f.columns:
        cond |= ~f.location_type.isin([0, np.nan])
    feed.stops = f[cond].copy()

    # Remove undefined parent stations from the ``parent_station`` column
    if "parent_station" in feed.stops.columns:
        f = feed.stops.copy()
        ids = f.stop_id.unique()
        f["parent_station"] = f.parent_station.map(
            lambda x: x if x in ids else np.nan
        )
        feed.stops = f

    # Drop trips with no stop times
    ids = feed.stop_times["trip_id"].unique()
    f = feed.trips
    feed.trips = f[f["trip_id"].isin(ids)]

    # Drop shapes with no trips
    ids = feed.trips["shape_id"].unique()
    f = feed.shapes
    if f is not None:
        feed.shapes = f[f["shape_id"].isin(ids)]

    # Drop routes with no trips
    ids = feed.trips["route_id"].unique()
    f = feed.routes
    feed.routes = f[f["route_id"].isin(ids)]

    # Drop services with no trips
    ids = feed.trips["service_id"].unique()
    if feed.calendar is not None:
        f = feed.calendar
        feed.calendar = f[f["service_id"].isin(ids)]
    if feed.calendar_dates is not None:
        f = feed.calendar_dates
        feed.calendar_dates = f[f["service_id"].isin(ids)]

    return feed


def clean_route_short_names(feed: "Feed") -> "Feed":
    """
    In ``feed.routes``, assign 'n/a' to missing route short names and
    strip whitespace from route short names.
    Then disambiguate each route short name that is duplicated by
    appending '-' and its route ID.
    Return the resulting Feed.
    """
    feed = feed.copy()
    r = feed.routes
    if r is None:
        return feed

    # Fill NaNs and strip whitespace
    r["route_short_name"] = r["route_short_name"].fillna("n/a").str.strip()

    # Disambiguate
    def disambiguate(row):
        rsn, rid = row
        return rsn + "-" + rid

    r["dup"] = r["route_short_name"].duplicated(keep=False)
    r.loc[r["dup"], "route_short_name"] = r.loc[
        r["dup"], ["route_short_name", "route_id"]
    ].apply(disambiguate, axis=1)
    del r["dup"]

    feed.routes = r
    return feed


def aggregate_routes(
    feed: "Feed", by: str = "route_short_name", route_id_prefix: str = "route_"
) -> "Feed":
    """
    Aggregate routes by route short name, say, and assign new route IDs using the
    given prefix.

    More specifically, the result is built from the given Feed as follows.
    Group ``feed.routes`` by the ``by`` column, and for each group

    1. Choose the first route in the group
    2. Assign a new route ID based on the given ``route_id_prefix``
       string and a running count, e.g. ``'route_013'``
    3. Assign all the trips associated with routes in the group to
       that first route
    4. Update the route IDs in the other "Feed" tables

    """
    if by not in feed.routes.columns:
        raise ValueError(f"Column {by} not in feed.routes")

    feed = feed.copy()

    # Create new route IDs
    routes = feed.routes
    n = routes.groupby(by).ngroups
    k = int(math.log10(n)) + 1  # Number of digits for padding IDs
    nrid_by_orid = dict()
    i = 1
    for col, group in routes.groupby(by):
        nrid = f"route_{i:0{k}d}"
        d = {orid: nrid for orid in group["route_id"].values}
        nrid_by_orid.update(d)
        i += 1

    routes["route_id"] = routes["route_id"].map(lambda x: nrid_by_orid[x])
    routes = routes.groupby(by).first().reset_index()
    feed.routes = routes

    # Update route IDs of trips
    trips = feed.trips
    trips["route_id"] = trips["route_id"].map(lambda x: nrid_by_orid[x])
    feed.trips = trips

    # Update route IDs of transfers
    if feed.transfers is not None:
        transfers = feed.transfers
        transfers["route_id"] = transfers["route_id"].map(
            lambda x: nrid_by_orid[x]
        )
        feed.transfers = transfers

    return feed


def clean(feed: "Feed") -> "Feed":
    """
    Apply the following functions to the given Feed in order and return the resulting
    Feed.

    1. :func:`clean_ids`
    2. :func:`clean_times`
    3. :func:`clean_route_short_names`
    4. :func:`drop_zombies`

    """
    feed = feed.copy()
    ops = [
        "clean_ids",
        "clean_times",
        "clean_route_short_names",
        "drop_zombies",
    ]
    for op in ops:
        feed = globals()[op](feed)

    return feed


def drop_invalid_columns(feed: "Feed") -> "Feed":
    """
    Drop all DataFrame columns of the given Feed that are not
    listed in the GTFS.
    Return the resulting Feed.
    """
    feed = feed.copy()
    for table, group in cs.GTFS_REF.groupby("table"):
        f = getattr(feed, table)
        if f is None:
            continue
        valid_columns = group["column"].values
        for col in f.columns:
            if col not in valid_columns:
                print(f"{table}: dropping invalid column {col}")
                del f[col]
        setattr(feed, table, f)

    return feed
