import utils
import gzip
import grpcpb.ForecastBatch_pb2 as forecastbatch
import pandas as pd
import numpy as np
import pyproj
# Here are defined all the parameters of the simulation.
files = ['data/rap_130_20160219_1200_000.grb2',  # 0
         'data/rap_130_20160415_0000_000.grb2',  # 1
         'data/rap_130_20160219_0000_000.grb2',  # 2
         'data/rap_130_20160415_1200_000.grb2',  # 3
         'data/rap_130_20160819_0000_000.grb2',  # 4
         'data/rap_130_20160819_1200_000.grb2']  # 5
filename = files[0]

# Old method creates the graph on startup (slower)
# New method creates the graph during A-star only in needed area (faster)
methods = ["new",       # 0
           "old"]       # 1
method = methods[0]


# Minimise fuel or distance.
heuristics = ["fuel",       # 0
              "distance",   # 1
              "DoP"]        # 2
heuristic = heuristics[2]

# Choose number of neighbours for each node
k_neighbours = 100

# Number of nodes on closest path to great-circle path. Only useful when calling main.closest(...) function
cpath_modu = 66  # useful for number of points in closest path

# Ground speed of the aircraft. When faster, the wind has less influence on the path.
ground_speed = 25  # m/s


# Factor to see the influence of more or less wind. Not really useful.
k_wind = 1



def read_forecast(filename):
    with gzip.open(filename, "rb") as f:
        data = f.read()
        batchset = forecastbatch.ForecastBatch()
        batchset.ParseFromString(data)
        return batchset


batch = read_forecast("forecasts/los_1_571595_4402060.bin")

points = batch.los.points

def point_wgs84_coordinates(points):
    return pd.DataFrame([
        dict(
            latitude=coordinate.position.latitude_deg,
            longitude=coordinate.position.longitude_deg,
            height=coordinate.height_m)
        for coordinate in points.point_wgs84])

wgs84 = point_wgs84_coordinates(points)

def dop_band_for_time(dop, time):
    period = 0
    if len(dop.valid_from) > 1:
        while dop.valid_from[period + 1] <= time:
            period += 1

    return dop.band[period]



def dop_bands_for_time(dop, time):
    return [dop_band_for_time(dop_point, time) for dop_point in dop.bands]


time = 000

dopbatch = read_forecast("forecasts/dop_1_571595_4402060.bin")
dops = dop_bands_for_time(dopbatch.dop, time)

df = pd.DataFrame([
    dict(x=dopbatch.dop.points.point_xy[i].x,
         y=dopbatch.dop.points.point_xy[i].y,
         dop=dop)
    for i, dop in enumerate(dops)])
#df.sort_values(by=['y'])
dop = df.iloc[:]['dop'].to_numpy()

ss = np.random.randint(len(df))
ee = np.random.randint(len(df))
if ss == ee:
    ee = np.random.randint(len(df))


start = 'a'
end = 'b'
start_dop = dop[ss]
end_dop = dop[ee]

target_srs_epsg = 4326

# Get point config and indices from forecast batch
points = batch.los.points
point_config = points.point_grid_configuration
point_indices = points.point_indices

# Create transformation from target SRS to grid SRS
target_crs = pyproj.CRS.from_epsg(target_srs_epsg)
batch_crs = pyproj.CRS.from_epsg(point_config.grid_srs_epsg)
target_to_batch_crs = pyproj.Transformer.from_crs(target_crs, batch_crs)

# Convert target to x,y of grid SRS
x, y = target_to_batch_crs.transform(wgs84.iloc[:]['latitude'].to_numpy(), wgs84.iloc[:]['longitude'].to_numpy())

# Calculate offset from grid reference
offset_x = x - point_config.offset_x
offset_y = y - point_config.offset_y

# Calculate grid coordinates using offset from grid and grid resolution
grid_x = df.iloc[:]['x'] #offset_x / point_config.resolution
grid_y = df.iloc[:]['y'] #offset_y / point_config.resolution

wgs84 = pd.concat([wgs84, df.iloc[:]['dop']], axis=1, join='inner')

start_latlon = wgs84.iloc[2862]['latitude'], wgs84.iloc[2862]['longitude'], wgs84.iloc[2862]['height'], wgs84.iloc[2862]['dop']
end_latlon = wgs84.iloc[990]['latitude'], wgs84.iloc[990]['longitude'], wgs84.iloc[990]['height'], wgs84.iloc[990]['dop']

# start_latlon = df.iloc[ss]['x'], df.iloc[ss]['y']
# end_latlon = df.iloc[ee]['x'], df.iloc[ee]['y']


# start_latlon = point_wgs84_coordinates(start_latlong)
# end_latlon = point_wgs84_coordinates(end_latlong)

# # Path color on figure.
utils.path_color = "red"

print("From " + start + " to " + end)
