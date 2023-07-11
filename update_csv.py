import json
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool
from shapely.geometry import shape

PARALLEL_PROCESSES = 16
ROUNDING_PRECISION = 3

# Constant to add to all calculations since NZZ omits Crimea from
# Russian-occupied Ukraine
CRIMEA_AREA = 26689.32  # in sqkm

EXPORT_FILE = 'territory.csv'

# nzz['territory'] = nzz['territory'] + CRIMEA_AREA

try:
    previous = pd.read_csv(EXPORT_FILE, parse_dates=True)
    previous.index = pd.to_datetime(previous.date.values).to_pydatetime()
    previous = previous.drop(columns=['date'])
except FileNotFoundError:
    previous = pd.DataFrame(columns=['area'])

def load_json(filename):
    with open('data/' + filename, 'r') as f:
        return json.load(f)

def compute_occupied_area(features):
    """
    Returns occupied area for list of features in square km
    """
    occupied = features
    geom = [shape(i['geometry']) for i in occupied]
    gdf = gpd.GeoDataFrame({'geometry': geom}, crs='EPSG:4326')
    # https://stackoverflow.com/questions/38961816/geopandas-set-crs-on-points
    #gdf = gdf.to_crs('EPSG:3857')  # convert to metric projection
    # Use CEA instead:
    gdf = gdf.to_crs({'proj': 'cea'})
    # https://gis.stackexchange.com/questions/254413/how-to-fix-hole-lies-outside-shell
    # https://gis.stackexchange.com/questions/253224/geopandas-buffer-using-geodataframe-while-maintaining-the-dataframe
    gdf['geometry'] = gdf.geometry.buffer(0)
    joined = gdf.dissolve(by=None)
    return float(round(joined.area[0], 2) / 1e6) + CRIMEA_AREA

def process_item(args):
    idx, filename = args
    print(f"(Processing {idx}", end='\r')

    data = load_json(filename)
    id_ = filename.split('.json')[0]
    date = datetime.strptime(id_, '%Y-%m-%d')

    # https://gis.stackexchange.com/questions/329349/calculating-the-area-by-square-feet-with-geopandas
    area = compute_occupied_area(data['value']['features'])
    return [id_, date, area, data['value']['features']]


files = sorted(os.listdir('data'))
to_process = []
for filename in files:
    if not datetime.strptime(filename.split('.json')[0], '%Y-%m-%d') in previous.index:
        to_process.append(filename)

def dispatch(items):
    print(f"Processing all {len(items)} items...")
    return list(ThreadPool(
        PARALLEL_PROCESSES).imap_unordered(process_item, enumerate(items, 1)))


# XXX this may be slow, takes about 2min on first run
processed = dispatch(to_process[:])

df = pd.DataFrame(processed, columns=['id', 'date', 'area', 'features'])
df = df.drop(['id'], axis=1)
df = df.sort_values(by='date', ascending=True)
df = df.set_index('date')

df['area'] = df['area'].astype('float').round(ROUNDING_PRECISION)
# Calculate change to previous day which translates to daily gains/losses
df['change'] = df['area'].diff()

adjusted = df.copy()
# Fix outliers
#adjusted['2022-05-15':'2022-05-19'] = adjusted[adjusted.index == '2022-05-14'].values
#adjusted.loc[adjusted.index == '2022-08-25'] = adjusted[adjusted.index == '2022-08-24'].values
# Recompute changed area
adjusted['change'] = adjusted['area'].diff()

combined = pd.DataFrame(pd.concat([previous['area'], adjusted['area']]))
combined.index.name = 'date'

# Apparently in March 2022 a few duplicates appear, normalize them
#combined = combined.resample('1d').mean()

# Round all values, including previous ones
combined['area'] = combined['area'].round(ROUNDING_PRECISION)

combined = combined.sort_index(ascending=True)

# Save all computed area figures to .csv file
combined['area'].to_csv(EXPORT_FILE, date_format='%Y-%m-%d %H:%M:%S')
