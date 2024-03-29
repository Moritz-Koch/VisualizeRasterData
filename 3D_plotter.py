import copy
import numpy as np
import rasterio
import plotly.graph_objects as go

### choose glacier and resolution ##
glacier_data_maps = 'Rhone_data_maps'
res = 1
#glacier_data_maps = 'Perito_data_maps'
#res = 10
####################################

# load data maps
elevation_rast = rasterio.open(glacier_data_maps + '/elevation.tif')
thickness_rast = rasterio.open(glacier_data_maps + '/thickness.tif')
outlines_rast = rasterio.open(glacier_data_maps + '/outlines.tif')
velocity_rast = rasterio.open(glacier_data_maps + '/velocity.tif')

# get lat and lon von axis
left, bottom, right, top = elevation_rast.bounds[0:4]
(res_lat, res_lon) = elevation_rast.res
lat_range = np.arange(left, right, res_lat)
lon_range = np.arange(bottom, top, res_lon)

# convert to numpy array asn mirror left to right
elevation = elevation_rast.read(1)[::-1, :].astype(np.float32)
thickness = thickness_rast.read(1)[::-1, :].astype(np.float32)
outlines = outlines_rast.read(1)[::-1, :].astype(np.float32)
velocity = velocity_rast.read(1)[::-1, :].astype(np.float32)

# compute bedrock and glacier surface
elevation[elevation <= 0] = None
thickness[thickness <= 0] = 0
bedrock = elevation - thickness
glacier_surface = copy.copy(elevation)
glacier_surface[outlines == 0] = None

thickness[outlines == 0] = None
velocity[outlines == 0] = None
velocity[velocity < 0] = None

# creat 3D plot
bedrock_fig = go.Surface(z=bedrock[::res, ::res], x=lat_range[::res], y=lon_range[::res], colorscale='speed_r'
                         , showlegend=True, name='bedrock',
                         colorbar=dict(x=-.2, title="elevation [m]", titleside='right'))

surface_fig = go.Surface(z=glacier_surface[::res, ::res], x=lat_range[::res], y=lon_range[::res], colorscale='Blues',
                         surfacecolor=thickness[::res, ::res], showlegend=True, name='glacier surface',
                         colorbar=dict(title="thickness in m", titleside='right'), )

fig_dict = {"data": [bedrock_fig, surface_fig]}
fig = go.Figure(fig_dict)

# compute aspect ratio of the base
max_bedrock = np.max(bedrock)
min_bedrock = np.min(bedrock)
resolution = int(lat_range[1] - lat_range[0])
ratio_y = bedrock.shape[0] / bedrock.shape[1]
ratio_z = (max_bedrock - min_bedrock) / (bedrock.shape[0] * resolution)
ratio_z *= 2  # emphasize z-axis to make mountians look twice as steep

fig.update_layout(title=glacier_data_maps, autosize=False, legend={'orientation': 'h'},
                  width=1000, height=1000, scene_aspectratio={"x": 1, "y": ratio_y, "z": ratio_z},
                  scene=dict(xaxis=dict(range=[lat_range[0], lat_range[-1]]),
                             yaxis=dict(range=[lon_range[0], lon_range[-1]]),
                             zaxis=dict(range=[min_bedrock, max_bedrock])))

fig.show()
