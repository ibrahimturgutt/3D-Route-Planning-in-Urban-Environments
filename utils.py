import numpy as np
import matplotlib.pyplot as plt
import geopandas
import pandas as pd
import pyproj
from shapely.geometry import LineString
import startup as su
import csv
import model
import params


path_color = 'grey'


def print_full_array(a):
    with np.printoptions(threshold=np.inf):
        print(a)


def check_path(nodes, path):
    """Check if path is valid. Not useful."""
    for n in path:
        print(n.id)

    for i in range(len(path) - 1):
        current = nodes[path[i].id]
        nextnode = nodes[path[i + 1].id]
        print(current.is_neighbour(nextnode))


def plot_path(path, explored, filename):
    """Plot path on screen or save path to tikz figure in filename.tex."""

    lats = [node.latlon[0] for node in path]
    lons = [node.latlon[1] for node in path]
    hs = [node.latlon[2] for node in path]
    
    lat_0e = [path[0].latlon[0], path[-1].latlon[0]]
    lon_0e = [path[0].latlon[1], path[-1].latlon[1]]
    h_0e = [path[0].latlon[2], path[-1].latlon[2]]

    lat_explored = [node.latlon[0] for node in explored]
    lon_explored = [node.latlon[1] for node in explored]
    h_explored = [node.latlon[2] for node in explored]

    df = pd.DataFrame(
        {
            'Latitude': lats,
            'Longitude': lons,
            'Heights': hs
        })
    
    df_0e = pd.DataFrame(
        {
            'Latitude': lat_0e,
            'Longitude': lon_0e,
            'Heights': h_0e
        })

    df_explored = pd.DataFrame(
        {
            'Latitude': lat_explored,
            'Longitude': lon_explored,
            'Heights': h_explored
        })

    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude, df.Heights))
    
    
    
    gdf_0e = geopandas.GeoDataFrame(
        df_0e, geometry=geopandas.points_from_xy(df_0e.Longitude, df_0e.Latitude, df_0e.Heights))
    
        
        
    
    gdf_explored = geopandas.GeoDataFrame(
        df_explored, geometry=geopandas.points_from_xy(df_explored.Longitude, df_explored.Latitude, df_explored.Heights))
    
    
    # world = geopandas.read_file(
    #     geopandas.datasets.get_path('naturalearth_lowres'))

    # # Plots map.
    # ax = world[world.continent == 'North America'].plot(
    #     color='white', edgecolor='black')
    
    
    # world = geopandas.read_file(
    #     geopandas.datasets.get_path('naturalearth_lowres'))

    # # Plots map.
    # ax = world[world.continent == 'North America'].plot(
    #     color='white', edgecolor='black')
    # first = [1, 2, 3, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90]
    # second = [571595, 571695, 571795, 571895, 571995, 572095, 572195, 572295, 572395, 572495]
    # third = [4401960, 4402060, 4402160, 4402260, 4402360, 4402460, 4402560, 4402660, 4402760, 4402860]
    # los = "los"
    # binf = ".bin"
    # us = "_"
    # files = []
    # for i in first:
    #     for j in second:
    #         for k in third:
    #             file_name = "forecasts/los_" + str(i) + "_" + str(j) + "_" + str(k) + ".bin"
    #             files.append(file_name)
                    
    # batch = []
    # for i in range(len(files)):
    #     bb = params.read_forecast(files[i])
    #     batch.append(bb)
    
            
    #batch = params.read_forecast(files)
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
        
    #batch = params.read_forecast("forecasts/los_1_571595_4402060.bin")
    
    
    # world = geopandas.read_file("data1/indianapolis-indiana-neighborhoods.shp")
    pts = point_wgs84_coordinates(params.points)
 
    
    gpts = geopandas.GeoDataFrame(
        pts, geometry=geopandas.points_from_xy(pts.longitude, pts.latitude, pts.height))
    

    
    
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(gpts['longitude'], gpts['latitude'], gpts['height'])
    ax.plot(gdf['Longitude'], gdf['Latitude'], gdf['Heights'], color='black', markersize=15)
    ax.scatter(gdf_0e['Longitude'][0], gdf_0e['Latitude'][0], gdf_0e['Heights'][0], color='orange', marker='o')
    ax.scatter(gdf_0e['Longitude'][1], gdf_0e['Latitude'][1], gdf_0e['Heights'][1], color='orange', marker='x')
    
    longgs = [gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0]]
    latts = [gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0]]
    hhs = [gdf_0e['Heights'][0], gdf_0e['Heights'][0]-10, gdf_0e['Heights'][0]-20, gdf_0e['Heights'][0]-30, gdf_0e['Heights'][0]-40, gdf_0e['Heights'][0]-50, gdf_0e['Heights'][0]-60]

    df_01e = pd.DataFrame(
        {
            'Latitude': latts,
            'Longitude': longgs,
            'Heights': hhs
        })
    gdf_01e = geopandas.GeoDataFrame(
        df_01e, geometry=geopandas.points_from_xy(df_01e.Longitude, df_01e.Latitude, df_01e.Heights))
    ax.plot(gdf_01e['Longitude'], gdf_01e['Latitude'], gdf_01e['Heights'], color='black', markersize=15)

    longgs = [gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0], gdf_0e['Longitude'][0]]
    latts = [gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0], gdf_0e['Latitude'][0]]
    hhs = [gdf_0e['Heights'][0], gdf_0e['Heights'][0]-10, gdf_0e['Heights'][0]-20, gdf_0e['Heights'][0]-30, gdf_0e['Heights'][0]-40, gdf_0e['Heights'][0]-50, gdf_0e['Heights'][0]-60]

    df_01e = pd.DataFrame(
            {
                'Latitude': latts,
                'Longitude': longgs,
                'Heights': hhs
            })
    gdf_01e = geopandas.GeoDataFrame(
            df_01e, geometry=geopandas.points_from_xy(df_01e.Longitude, df_01e.Latitude, df_01e.Heights))
    ax.plot(gdf_01e['Longitude'], gdf_01e['Latitude'], gdf_01e['Heights'], color='black', markersize=15)
        
        
    longgs = [gdf_0e['Longitude'][1], gdf_0e['Longitude'][1], gdf_0e['Longitude'][1], gdf_0e['Longitude'][1], gdf_0e['Longitude'][1], gdf_0e['Longitude'][1], gdf_0e['Longitude'][1]]
    latts = [gdf_0e['Latitude'][1], gdf_0e['Latitude'][1], gdf_0e['Latitude'][1], gdf_0e['Latitude'][1], gdf_0e['Latitude'][1], gdf_0e['Latitude'][1], gdf_0e['Latitude'][1]]
    hhs = [gdf_0e['Heights'][1], gdf_0e['Heights'][1]-10, gdf_0e['Heights'][1]-20, gdf_0e['Heights'][1]-30, gdf_0e['Heights'][1]-40, gdf_0e['Heights'][1]-50, gdf_0e['Heights'][1]-60]

    df_01e = pd.DataFrame(
        {
            'Latitude': latts,
            'Longitude': longgs,
            'Heights': hhs
        })
    gdf_01e = geopandas.GeoDataFrame(
        df_01e, geometry=geopandas.points_from_xy(df_01e.Longitude, df_01e.Latitude, df_01e.Heights))
    ax.plot(gdf_01e['Longitude'], gdf_01e['Latitude'], gdf_01e['Heights'], color='black', markersize=15)
    
    
    b = 0.99986
    e = 0.01671
    a = b/np.sqrt(1-e**2)
    p = 13
    alpha = np.arctan((gdf.iloc[-1]['Latitude']-gdf.iloc[0]['Latitude'])/(gdf.iloc[-1]['Longitude']-gdf.iloc[0]['Longitude']))
    N = a/(np.sqrt(1-(e**2)*np.sin(gdf['Latitude'])**2))
        
    
    lat1 = (np.arctan(gdf['Heights']/(1-e**2)*p))*np.cos(alpha)/111000
    lon1 = alpha/111000#(np.arctan(np.cos(alpha)/np.sin(alpha)))/1000
    h1 = ((1-e**2)*N+gdf['Heights'])*np.sin(gdf['Latitude'])
    
    x1 = pd.concat([gdf['Longitude']-lon1, gdf['Longitude']+lon1], axis=0, join='inner')
    y1 = pd.concat([gdf['Latitude']+lat1, gdf['Latitude']-lat1], axis=0, join='inner')
    z = (h1/np.sin(gdf['Latitude']))-(1-e**2)*N
    z1 = pd.concat([z, z], axis=0, join='inner')
    
    

    
    p2 = 1.25
    lat2 = (np.arctan(gdf['Heights']/(1-e**2)*p2))*np.cos(alpha)/111000
    lon2 = alpha/111000
    
    
    
    x2 = gdf['Longitude']-lon1-lon2
    y2 = gdf['Latitude']+lat1+lat2
    
    x2 = pd.concat([gdf['Longitude']-lon1, x2], axis=0, join='inner')
    y2 = pd.concat([gdf['Latitude']+lat1, y2], axis=0, join='inner')
    
    
    
    x3 = gdf['Longitude']+lon1+lon2
    y3 = gdf['Latitude']-lat1-lat2
    
    x3 = pd.concat([gdf['Longitude']+lon1, x3], axis=0, join='inner')
    y3 = pd.concat([gdf['Latitude']-lat1, y3], axis=0, join='inner')
    
    
    
    p3 = 0.25
    lat3 = (np.arctan(gdf['Heights']/(1-e**2)*p3))*np.cos(alpha)/111000
    lon3 = alpha/111000
    
    x4 = gdf['Longitude']-lon1-lon2-lon3
    y4 = gdf['Latitude']+lat1+lat2+lat3
    
    x4 = pd.concat([gdf['Longitude']-lon1-lon2, x4], axis=0, join='inner')
    y4 = pd.concat([gdf['Latitude']+lat1+lat2, y4], axis=0, join='inner')
    
    
    
    x5 = gdf['Longitude']+lon1+lon2+lon3
    y5 = gdf['Latitude']-lat1-lat2-lat3
    
    x5 = pd.concat([gdf['Longitude']+lon1+lon2, x5], axis=0, join='inner')
    y5 = pd.concat([gdf['Latitude']-lat1-lat2, y5], axis=0, join='inner')
    
    
    ax.plot_trisurf(x1, y1, z1, color='green', alpha=0.3)    
    ax.plot_trisurf(x2, y2, z1, color='yellow', alpha=0.3)
    ax.plot_trisurf(x3, y3, z1, color='yellow', alpha=0.3)
    ax.plot_trisurf(x4, y4, z1, color='red', alpha=0.3)
    ax.plot_trisurf(x5, y5, z1, color='red', alpha=0.3)
    
    ax.scatter(x1, y1, z1-8, color='green', alpha=.3)
    ax.scatter(x1, y1, z1+8, color='green', alpha=.3)
    ax.scatter(x2, y2, z1-8, color='yellow', alpha=.3)
    ax.scatter(x2, y2, z1+8, color='yellow', alpha=.3)
    ax.scatter(x3, y3, z1-8, color='yellow', alpha=.3)
    ax.scatter(x3, y3, z1+8, color='yellow', alpha=.3)
    ax.scatter(x4, y4, z1-8, color='red', alpha=.3)
    ax.scatter(x4, y4, z1+8, color='red', alpha=.3)
    ax.scatter(x5, y5, z1-8, color='red', alpha=.3)
    ax.scatter(x5, y5, z1+8, color='red', alpha=.3)
    
    ax.scatter(x1, y1, z1-8-0.75, color='yellow', alpha=.3)
    ax.scatter(x1, y1, z1+8+0.75, color='yellow', alpha=.3)
    ax.scatter(x2, y2, z1-8-0.75, color='yellow', alpha=.3)
    ax.scatter(x2, y2, z1+8+0.75, color='yellow', alpha=.3)
    ax.scatter(x3, y3, z1-8-0.75, color='yellow', alpha=.3)
    ax.scatter(x3, y3, z1+8+0.75, color='yellow', alpha=.3)
    ax.scatter(x4, y4, z1-8-0.75, color='yellow', alpha=.3)
    ax.scatter(x4, y4, z1+8+0.75, color='yellow', alpha=.3)
    ax.scatter(x5, y5, z1-8-0.75, color='yellow', alpha=.3)
    ax.scatter(x5, y5, z1+8+0.75, color='yellow', alpha=.3)
    
    ax.scatter(x1, y1, z1-8-0.75-0.25, color='red', alpha=.3)
    ax.scatter(x1, y1, z1+8+0.75+0.25, color='red', alpha=.3)
    ax.scatter(x2, y2, z1-8-0.75-0.25, color='red', alpha=.3)
    ax.scatter(x2, y2, z1+8+0.75+0.25, color='red', alpha=.3)
    ax.scatter(x3, y3, z1-8-0.75-0.25, color='red', alpha=.3)
    ax.scatter(x3, y3, z1+8+0.75+0.25, color='red', alpha=.3)
    ax.scatter(x4, y4, z1-8-0.75-0.25, color='red', alpha=.3)
    ax.scatter(x4, y4, z1+8+0.75+0.25, color='red', alpha=.3)
    ax.scatter(x5, y5, z1-8-0.75-0.25, color='red', alpha=.3)
    ax.scatter(x5, y5, z1+8+0.75+0.25, color='red', alpha=.3)
    
    params.df.plot.scatter(x="x", y="y", c="dop", colormap="RdYlGn_r", s=100)
    
    

    # # Computes great-circle.
    # great_circle = great_circle_path(path[0], path[-1])
    
    # # Plot great-circle.
    # great_circle.plot(ax=ax, color='blue')
    


    # ax.set_xlim(-86.1993, -86.1278)
    # ax.set_ylim(39.7491, 39.8018)
    plt.title('Indianapolis')
    ax.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
    plt.xticks([])
    plt.yticks([])
    ax.set_ylabel('Latitude')
    ax.set_xlabel('Longitude')
    ax.set_zlabel('Height')
    



    # Show path on screen.
    plt.show()

    # Uncomment to save path to tikz figure.
    #tikzplotlib.save(filename + ".tex")



def reinit(nodes):
    """Re-initialise nodes to run the algorithm another time."""
    for node in nodes:
        node.pred = None
        node.fscore = float('inf')
        node.gscore = float('inf')


def print_fscore(i, path):
    node = path[i]
    for neighbour in node.neighbours:
        n = neighbour.node
        print(str(n.fscore) + ", " + str(n in path) +
              ", " + str(n.gscore) + ", id: " + str(n.id))


def print_fscore_g(i, g, path):

    node = g[i]
    for neighbour in node.neighbours:
        n = neighbour.node
        print(str(n.fscore) + ", " + str(n in path) +
              ", " + str(n.gscore) + ", id: " + str(n.id))


def min_tri(i, g, path):
    s = path[0]
    n = g[i]
    e = path[-1]
    return s.get_distance_to(n) + n.get_distance_to(e)


def great_circle_path(s, e):
    """Computes great circle trajectory."""
    start_latlon = s.latlon
    end_latlon = e.latlon

    startlong = start_latlon[1]
    startlat = start_latlon[0]
    endlong = end_latlon[1]
    endlat = end_latlon[0]

    # calculate distance between points
    g = pyproj.Geod(ellps='WGS84')
    (_, _, dist) = g.inv(startlong, startlat, endlong, endlat)

    # calculate line string along path with segments <= 1 km
    lonlats = g.npts(startlong, startlat, endlong, endlat,
                     1 + int(dist / 1000))

    # npts doesn't include start/end points, so prepend/append them
    lonlats.insert(0, (startlong, startlat))
    lonlats.append((endlong, endlat))

    l = LineString(lonlats)
    g = geopandas.GeoSeries(l)
    return g


def path_len(path):
    """Computes path length."""
    d = 0
    for i in range(len(path) - 1):
        d += path[i].get_distance_to_gc(path[i+1])
    return d


def closest_path(s, e, nodes, modu=600):
    """Finds closest path to the great-circle using the grid from the grb2 file."""
    l = list(great_circle_path(s, e)[0].coords)
    cpath = [s]
    k = len(l)
    for pr in range(0, k, modu):
        pnode = nodes[su.find_closest(nodes, [l[pr][1], l[pr][0]], 0)]

        if not pnode in cpath:
            cpath.append(pnode)
    if e not in cpath:
        cpath.append(e)
    return cpath


def load_cities_latlon(filename):
    """Load cities csv."""
    cities = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cities.setdefault(row['city_ascii'], [
                float(row['lat']), float(row['lng'])])
    return cities


def path_fuel_cost(path):
    """Computes fuel cost of path."""
    c = 0
    for i in range(len(path) - 1):
        c += model.get_fuel_cost(path[i], path[i+1], "wind")
    return c

def path_dop_cost(dop):
    z = 0
    for i in range(len(dop) - 1):
        z += model.get_dop_cost(dop[i], dop[i+1])
    return z

def path_optim_cost(path, dop):
    t = 0
    for i in range(len(path) - 1):
        t += model.get_optim_cost(path[i].latlon[3], path[i+1].latlon[3], path[i], path[i+1], "wind")
    return t