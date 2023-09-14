from osgeo import gdal

# Boundary of Rhone
ulx, lry, lrx, uly = 449888.3, 5156658.9, 457636.3, 5168032.0   # these are the outer boundaries of the rhone glacier domain we want to plot
resolution = 100 # this sets the resolution (in m) which is adjustable if you want to downscale the plot options. downscaling enables faster plotting trading off resolution.

# INPUT files // raw data import
elevation_file = "Rhone_data_maps/raw_data/SwissALTI3D_r2019.tif"
thickness_file = "Rhone_data_maps/raw_data/IceThickness.tif"
velocity_file = "Rhone_data_maps/raw_data/V_RGI-11_2021July01.tif"
outlines_file = "Rhone_data_maps/raw_data/RGI6_Alps.tif"

# opening and warping files to desired resolution, extent and coordinate reference system (crs)
elevation = gdal.Open(elevation_file)
elevation_aligned_file = "Rhone_data_maps/elevation.tif"
gdal.Warp(elevation_aligned_file, elevation, srcSRS='EPSG:2056', dstSRS='EPSG:32632',
                           resampleAlg='bilinear', xRes=resolution, yRes=resolution,
                           outputBounds=(ulx, lry, lrx, uly))

thickness = gdal.Open(thickness_file)
thickness_aligned_file = "Rhone_data_maps/thickness.tif"
gdal.Warp(thickness_aligned_file, thickness, srcSRS='EPSG:2056', dstSRS='EPSG:32632',
                           resampleAlg='bilinear', xRes=resolution, yRes=resolution,
                           outputBounds=(ulx, lry, lrx, uly))

velocity = gdal.Open(velocity_file)
velocity_aligned_file = "Rhone_data_maps/velocity.tif"
gdal.Warp(velocity_aligned_file, velocity, srcSRS='EPSG:32632', dstSRS='EPSG:32632',
                           resampleAlg='bilinear', xRes=resolution, yRes=resolution,
                           outputBounds=(ulx, lry, lrx, uly))

outlines = gdal.Open(outlines_file)
outlines_aligned_file = "Rhone_data_maps/outlines.tif"
gdal.Warp(outlines_aligned_file, outlines, srcSRS='EPSG:2056', dstSRS='EPSG:32632',
                           resampleAlg='bilinear', xRes=resolution, yRes=resolution,
                           outputBounds=(ulx, lry, lrx, uly))