# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:15:47 2022

@author: İbrahim
"""

import gzip
import grpcpb.ForecastBatch_pb2 as forecastbatch


def read_forecast(filename):
    with gzip.open(filename, "rb") as f:
        data = f.read()
        batchset = forecastbatch.ForecastBatch()
        batchset.ParseFromString(data)
        return batchset


batch = read_forecast("forecasts/los_1_571595_4402060.bin")

import pandas as pd


def point_xy_coordinates(points):
    # Note: `point_xy` contains the grid _index_. As points are at the center of
    # a grid cell, 0.5 must be added to the index to convert the index to the
    # grid coordinate.
    return pd.DataFrame([
        dict(
            x=coordinate.x + 0.5,
            y=coordinate.y + 0.5)
        for coordinate in points.point_xy])


def plot_xy_coordinates(points):
    coords = point_xy_coordinates(points)
    coords.plot.scatter(
        x="x",
        y="y",
        grid=True,
        xticks=range(points.point_grid_configuration.size_x + 1),
        yticks=range(points.point_grid_configuration.size_y + 1),
        figsize=(6, 5))


plot_xy_coordinates(batch.los.points)

def point_wgs84_coordinates(points):
    return pd.DataFrame([
        dict(
            latitude=coordinate.position.latitude_deg,
            longitude=coordinate.position.longitude_deg,
            height=coordinate.height_m)
        for coordinate in points.point_wgs84])


def plot_wgs84_coordinates(points):
    coords = point_wgs84_coordinates(points)
    coords.plot.scatter(
        x="longitude",
        y="latitude",
        c="height",
        colormap="viridis",
        figsize=(6, 5))


plot_wgs84_coordinates(batch.los.points)

point_index = batch.los.points.point_indices.x[15].y[17]
sat_index = batch.los.satellites.satellite_indices.constellation[forecastbatch.Constellation.GPS].svid[13]

los = batch.los.satellite_los[sat_index].point_los[point_index]
periods = list(zip(los.los_from, los.los_to))
print(periods)

los = batch.los
num_satellites = los.satellites.num_satellites


def is_los(satellite_index, point_index, time):
    periods = los.satellite_los[satellite_index].point_los[point_index]
    is_time_in_period = [
        start <= time < end
        for (start, end) in zip(periods.los_from, periods.los_to)
    ]
    return any(is_time_in_period)


def satellite_str(id):
    constellation = forecastbatch.Constellation.keys()[id.constellation]
    svid = id.svid
    return f"{constellation} {svid}"


def los_set(point_index, time):
    return [
        satellite_str(batch.los.satellites.satellite_id[sat])
        for sat in range(num_satellites)
        if is_los(sat, point_index, time)
    ]


print(los_set(point_index, time=0))

azel_forecast = read_forecast("forecasts/azel_1_571595_4402060.bin")

sat_index = azel_forecast.az_el.satellites.satellite_indices.constellation[forecastbatch.Constellation.GPS].svid[1]
sat_azel = azel_forecast.az_el.az_el[sat_index]

df = pd.DataFrame([
    dict(time=time, azimuth=azimuth, elevation=elevation)
    for time, azimuth, elevation
    in zip(sat_azel.valid_from, sat_azel.azimuth_deg, sat_azel.elevation_deg)
])

df.plot.scatter(x="azimuth", y="elevation", c="time", colormap="viridis")

import pandas as pd


def dop_band_for_time(dop, time):
    period = 0
    while dop.valid_from[period + 1] <= time:
        period += 1
    return dop.band[period]


def dop_bands_for_time(dop, time):
    return [dop_band_for_time(dop_point, time) for dop_point in dop.bands]


time = 5000
dopbatch = read_forecast("forecasts/dop_1_571595_4402060.bin")
dops = dop_bands_for_time(dopbatch.dop, time)

df = pd.DataFrame([
    dict(x=dopbatch.dop.points.point_xy[i].x,
         y=dopbatch.dop.points.point_xy[i].y,
         dop=dop)
    for i, dop in enumerate(dops)])

df.plot.scatter(x="x", y="y", c="dop", colormap="RdYlGn_r", s=100)