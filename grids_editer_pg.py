## create land and ocean masks and add points near to single grid points


import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
import os

path_src_grid='input.nc' # Path of your input grid file to be edited 
path_edit_gr='output.txt' # Path of the output text file

## Identifying singlular grid points

ds=xr.open_dataset(path_src_grid).wet+1
ds=ds.where(ds==1).fillna(0)

hh=ds.where(
    (ds == 1) &
    (ds.shift(grid_x_T=1,fill_value=0) == 0) & (ds.shift(grid_x_T=-1,fill_value=0) == 0) &
    (ds.shift(grid_y_T=1,fill_value=0) == 0) & (ds.shift(grid_y_T=-1,fill_value=0) == 0)
            )
lon_inf=np.where(hh==1)[1];lat_inf=np.where(hh==1)[0]

single_p_lon=[x+1 if x < len(ds.grid_x_T) else x-1 for x in lon_inf]
single_p_lat=[x if x < len(ds.grid_y_T) else x+1 if x == 0 else x-1 for x in lat_inf]
mask_df = pd.DataFrame([single_p_lon,single_p_lat,np.arange(len(lon_inf))*0],index=['lon','lat','mask']).T
##################################################################################################################################################
## Draw rectangles to create a land mask
ds=xr.open_dataset(path_src_grid)
coordinates_set1 = []

from matplotlib.widgets import Button, RectangleSelector
import csv
import numpy as np

def draw_set1_rectangles():
    # Create the image
    fig, ax = plt.subplots()
    a = np.arange(10)
    image = ax.contourf(np.arange(len(ds.grid_x_T)), np.arange(len(ds.grid_y_T)), ds.wet, levels=[0, 0.5, 1], colors=['black', 'lightblue'])
    ax.set_title('Draw the rectangles over the area to apply a land mask [depth =0] - close after selecting the region to proceed', fontweight="bold",loc='left')
    ax.tick_params(axis='both',labelsize=20)
    rectangles = []  # List to store the Rectangle objects

    def onselect(eclick, erelease):
        x1, y1 = int(round(eclick.xdata)), int(round(eclick.ydata))
        x2, y2 = int(round(erelease.xdata)), int(round(erelease.ydata))
        coordinates_set1.append((x1, x2, y1, y2))
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='r', facecolor='r', alpha=0.6)
        rectangles.append(rect)
        ax.add_patch(rect)
        plt.draw()

    def remove_last_rectangle(event):
        if rectangles:
            last_rectangle = rectangles.pop()
            last_rectangle.remove()
            coordinates_set1.pop()
            plt.draw()

    # Connect the RectangleSelector to the figure
    rs = RectangleSelector(ax, onselect)

    # Add a button to remove the last drawn rectangle
    remove_button_ax = plt.axes([0.8, 0.93, 0.15, 0.05])
    remove_button = Button(remove_button_ax, 'Remove last rectangle')
    remove_button.on_clicked(remove_last_rectangle)

    # Show the plot for drawing the first set of rectangles
    plt.show()

    # Save the coordinates of the first set to a CSV file
    with open('coordinates_set1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x1', 'x2', 'y1', 'y2'])
        writer.writerows(coordinates_set1)

## Function to ask if the user wants to draw a second set of rectangles
 
def ask_for_second_set():
    response = input("Do you want to apply an ocean mask? (yes/no): ")
    return response.lower() == "yes"

coordinates_set2 = []
# Function to draw the second set of rectangles
def draw_set2_rectangles():
    # Create the image again for the second set
    fig, ax = plt.subplots()
    a = np.arange(10)
    image = ax.contourf(np.arange(len(ds.grid_x_T)), np.arange(len(ds.grid_y_T)), ds.wet, levels=[0, 0.5, 1], colors=['black', 'lightblue'])
    ax.set_title('Draw the rectangles over the area to apply an ocean mask', fontweight="bold")
    ax.tick_params(axis='both',labelsize=20)

    rectangles = []  # List to store the Rectangle objects

    for coord in coordinates_set1:
        x1, x2, y1, y2 = coord
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='r', facecolor='r', alpha=0.6)
        rectangles.append(rect)
        ax.add_patch(rect)

    def onselect(eclick, erelease):
        x1, y1 = int(round(eclick.xdata)), int(round(eclick.ydata))
        x2, y2 = int(round(erelease.xdata)), int(round(erelease.ydata))
        coordinates_set2.append((x1, x2, y1, y2))
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='b', facecolor='b', alpha=0.6)
        rectangles.append(rect)
        ax.add_patch(rect)
        plt.draw()

    def remove_last_rectangle(event):
        if rectangles:
            last_rectangle = rectangles.pop()
            last_rectangle.remove()
            coordinates_set2.pop()
            plt.draw()

    # Connect the RectangleSelector to the figure
    rs = RectangleSelector(ax, onselect)

    # Add a button to remove the last drawn rectangle
    remove_button_ax = plt.axes([0.8, 0.93, 0.15, 0.05])
    remove_button = Button(remove_button_ax, 'Remove last recatangle')
    remove_button.on_clicked(remove_last_rectangle)

    # Show the plot for drawing the second set of rectangles
    plt.show()

    # Save the coordinates of the second set to a CSV file
    with open('coordinates_set2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x1', 'x2', 'y1', 'y2'])
        writer.writerows(coordinates_set2)

# Call the functions
draw_set1_rectangles()

if ask_for_second_set():
    draw_set2_rectangles()


# Create the final figure
fig, ax = plt.subplots()
a = np.arange(10)
image = ax.contourf(np.arange(len(ds.grid_x_T)),np.arange(len(ds.grid_y_T)),ds.wet,levels=[0,0.5,1],colors=['black','lightblue'])
ax.set_title('Applied masks [Red - Land] [Blue-ocean]' ,fontweight = "bold")
# Draw the rectangles from the first set
for coord in coordinates_set1:
    x1, x2, y1, y2 = coord
    rect = Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='r', facecolor='r', alpha=0.6)
    ax.add_patch(rect)

# Draw the rectangles from the second set
if os.path.isfile('coordinates_set2.csv'):
    for coord in coordinates_set2:
        x1, x2, y1, y2 = coord
        rect = Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='b', facecolor='b', alpha=0.6)
        ax.add_patch(rect)
from matplotlib.patches import Circle
for lon, lat in zip(lon_inf, lat_inf):
    circle = plt.Circle((lon, lat), 2.5, color='black',fill=False, alpha=0.3,ls='-',lw=1.5)
    ax.add_artist(circle)
# Show the final figure
plt.show()




dfn=pd.read_csv('coordinates_set1.csv').astype(str)
mask_df_1=pd.concat([dfn['x1']+':'+dfn['x2'],dfn['y1']+':'+dfn['y2']],axis=1)
mask_df_1.columns = ['lon','lat']
mask_df_1['mask']=0
	
if os.path.isfile('coordinates_set2.csv'):
    # Read the file using pandascoordinates_set2.csv

    dfm=pd.read_csv('coordinates_set2.csv').astype(str)
    mask_df_2=pd.concat([dfm['x1']+':'+dfm['x2'],dfm['y1']+':'+dfm['y2']],axis=1)
    mask_df_2.columns = ['lon','lat']
    mask_df_2['mask']=1
    pd.concat([mask_df,mask_df_1,mask_df_2]).reset_index(drop=True).to_csv(path_edit_gr,header=None,index=None,sep=',',quotechar=' ')
else:
    pd.concat([mask_df,mask_df_1]).reset_index(drop=True).to_csv(path_edit_gr,header=None,index=None,sep=',',quotechar=' ')

with open(path_edit_gr, 'r') as file:
    content = file.read()
    content = content.replace(',', ', ')

# Save the modified content back to the CSV file
with open(path_edit_gr, 'w') as file:
    file.write(content)
if os.path.isfile('coordinates_set2.csv'):
	os.remove('coordinates_set2.csv')
os.remove('coordinates_set1.csv')


