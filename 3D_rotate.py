import os
import copy
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import rasterio
import shutil

### choose glacier and resolution ##
#glacier_data_maps = 'Rhone_data_maps'
#res = 1
glacier_data_maps = 'Perito_data_maps'
res = 10
####################################

# load data maps
elevation_rast = rasterio.open(glacier_data_maps+'/elevation.tif')
outliness_rast = rasterio.open(glacier_data_maps+'/outlines.tif')

# get lat and lon von axis
left, bottom, right, top = elevation_rast.bounds[0:4]
(res_lat, res_lon) = elevation_rast.res
lat_range = np.arange(left, right, res_lat)
lon_range = np.arange(bottom, top, res_lon)

# convert to numpy array asn mirror left to right
elevation = elevation_rast.read(1)[::-1,:].astype(np.float32)
outliness = outliness_rast.read(1)[::-1,:].astype(np.float32)

X, Y = np.meshgrid(lat_range, lon_range)
elevation[outliness==0] = None

# create folder to store frames
if os.path.exists('frames'):
    shutil.rmtree('frames')
    os.mkdir('frames')
else:
    os.mkdir('frames')

# loop to create multiple frames
for i in np.arange(0,360,2):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Plot the surface.

    surf = ax.plot_surface(X, Y, elevation,cmap=cm.Blues_r)

    # change viewing angle in every iteration
    ax.view_init(30, i)
    ax.set_box_aspect((1, 1,0.5))  # aspect ratio is 1:1:1 in data space

    plt.savefig('frames/frame_%04i.png'%i)

import os
from PIL import Image

# get file names in correct order
dir = 'frames/'
files = os.listdir(dir)
files.sort()

# read all frames
frames = []
for image in files:
    if image.endswith('.png'):
        frames.append(Image.open(dir+image))

# append all frames to a gif
if not os.path.exists('plots'):
    os.mkdir('plots')

frame_one = frames[0]
frame_one.save("plots/glacier_rotate.gif", format="GIF", append_images=frames, save_all=True, duration=100, loop=0)