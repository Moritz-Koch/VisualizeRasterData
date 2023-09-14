# Author M.K.
# This script creates 2D-Hovmöller plots
# import
import pandas as pd
import matplotlib.pyplot as plt

# load your .csv file
df = pd.read_csv('Perito_data_maps/SurfaceVelo_Data/Strongbreen_BufferedExtraction.csv', sep=",")

# Set the first column as the index
df.set_index(df.columns[0], inplace=True)

# Extract the distance values from the first row
distance = df.columns[1:]

# Extract the date values from the index
dates = pd.to_datetime(df.index, format='%Y_%m').strftime('%Y-%m')

# Remove the first row from the DataFrame
df = df.iloc[:, 1:].astype(float)

# Create the Hovmöller plot
plt.imshow(df, cmap='viridis', aspect='auto')
plt.colorbar(label='surface velocity in m/day')
plt.xlabel('Distance')
plt.ylabel('Date')
plt.title('Hovmöller Plot')

# Set the tick labels for the x-axis (distance) # [::2] every 2nd extraction point
plt.xticks(range(len(distance))[::10], distance[::10], rotation=45)

# Set the tick labels for the y-axis (date) # [::6] every 6th month
plt.yticks(range(len(dates))[::6], dates[::6])

# Show the plot
plt.show()

# interpolate?
# multipanel -> https://www.cambridge.org/core/journals/journal-of-glaciology/article/recent-surging-event-of-a-glacier-on-geladandong-peak-on-the-central-tibetan-plateau/3D17FFC2AE116DFDC52CD6BF6AEE1613

