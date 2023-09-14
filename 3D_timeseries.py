import copy
import numpy as np
import rasterio
import plotly.graph_objects as go

### choose glacier and resolution ##
#glacier_data_maps = 'Rhone_data_maps'
#resolution_downscaling = 1
#lake_level = 0
glacier_data_maps = 'Perito_data_maps'
resolution_downscaling = 10
lake_level = 178
####################################

# load data maps
res = resolution_downscaling
elevation_rast = rasterio.open(glacier_data_maps + '/elevation.tif')
thickness_rast = rasterio.open(glacier_data_maps + '/thickness.tif')
outliness_rast = rasterio.open(glacier_data_maps + '/outlines.tif')

# get lat and lon von axis
left, bottom, right, top = elevation_rast.bounds[0:4]
(res_lat, res_lon) = elevation_rast.res
lat_range = np.arange(left, right, res_lat)
lon_range = np.arange(bottom, top, res_lon)

# convert to numpy array as mirror left to right
elevation = elevation_rast.read(1)[::-1, :].astype(np.float32)
thickness = thickness_rast.read(1)[::-1, :].astype(np.float32)
outliness = outliness_rast.read(1)[::-1, :].astype(np.float32)

# create a lake layer that has 'None' outside the elevation map
lake_surface = copy.copy(elevation)
lake_surface[elevation >= 0] = lake_level
lake_surface[elevation <= 0] = None

# compute bedrock and glacier surface
elevation[elevation <= 0] = None
thickness[thickness <= 0] = 200
bedrock = elevation - thickness
glacier_surface = copy.copy(elevation)
glacier_surface[outliness == 0] = None
thickness[outliness == 0] = None

# crop the lake layer to the area where bedrock is below lake_level
lake_surface[bedrock > lake_level] = None

frames = []
slider_steps = []
for year in np.arange(2000, 2100, 10):
        # update elevation data
        glacier_surface = np.subtract(glacier_surface, year/100)


        # create 3D plots with new data
        lake_fig = go.Surface(z=lake_surface[::res,::res], x=lat_range[::res], y=lon_range[::res], colorscale='Blues',
                                 opacity=.8, showlegend=True, name='lake',
                                 colorbar=dict(x=1.2, title="lake level [m]", titleside='right'))
        bedrock_fig = go.Surface(z=bedrock[::res, ::res], x=lat_range[::res], y=lon_range[::res], colorscale='speed_r',
                                 opacity=1, showlegend=True, name='bedrock',
                                 colorbar=dict(x=-.2, title="elevation [m]", titleside='right'))

        surface_fig = go.Surface(z=glacier_surface[::res, ::res], x=lat_range[::res], y=lon_range[::res],
                                 colorscale='Blues',
                                 surfacecolor=thickness[::res, ::res], showlegend=True, name='glacier surface',
                                 colorbar=dict(title="thickness [m]", titleside='right'), )


        # create frame
        frame = {"data": [bedrock_fig, surface_fig, lake_fig], "name": str(year)}
        frames.append(frame)

        # add slider step
        slider_step = {"args": [[year], {"frame": {"duration": 0, "redraw": True}, }],
                       "label": str(year), "method": "animate"}
        slider_steps.append(slider_step)

# add slider to layout
fig_dict = dict(data=frames[0]['data'],
                frames=frames,
                layout=dict(sliders=[{"steps": slider_steps, "y": 0}],
                            title=glacier_data_maps,
                            legend={"orientation": "h"},
                            width=1000, height=1000,
                            scene_aspectratio={"x": 1, "y": 1, "z": .3}))
fig = go.Figure(fig_dict)

fig.show()

