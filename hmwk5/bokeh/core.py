import random

import pandas as pd
from nbformat import read
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Dropdown
from bokeh.layouts import column
from bokeh.models import ColumnDataSource

# load data and format 
records = pd.read_csv('preprocessed_averages.csv')
records["zipcode"] = records["zipcode"].astype(str)

# to match csv
months =['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6', 'Month 7', 'Month 8', 'Month 9', 'Month 10', 'Month 11', 'Month 12']

# initilize to 0
source1 = ColumnDataSource(data=dict(x=months, y=[0]*12))
source2 = ColumnDataSource(data=dict(x=months, y=[0]*12))

# Extract the Total average row and convert it to a list
total_average_row = records[records['zipcode'] == 'Total Average']
if not total_average_row.empty:
    total_average = total_average_row.iloc[0].tolist()[1:]  # Exclude the zipcode column
else:
    total_average = [0] * 12  # Default to zeros if the row is not found
    
# make the source for total 
source_total = ColumnDataSource(data=dict(x=months, y=total_average))

# Create the figure
p = figure(title="Request Time Monthly Averages", x_axis_label='Month', y_axis_label='Average Response Time (hours)', x_range=months)
# plot the lines
p.line(x='x', y='y', source=source1, line_width=2, color='blue', legend_label='Zipcode 1')
p.line(x='x', y='y', source=source2, line_width=2, color='red', legend_label='Zipcode 2')
p.line(x='x', y='y', source=source_total, line_width=2, color='green', legend_label='Total Average')

# specific widget functions for the 2 zipcodes
def change_1(event):
    if event.item in records['zipcode'].values:
        new_y = records[records['zipcode'] == event.item].iloc[0][months].tolist()
        source1.data = dict(x=months, y=new_y)
    else:
        raise Exception(f'unknown item: {event.item}')
def change_2(event):
    if event.item in records['zipcode'].values:
        new_y = records[records['zipcode'] == event.item].iloc[0][months].tolist()
        source2.data = dict(x=months, y=new_y)
    else:
        raise Exception(f'unknown item: {event.item}')
    

valid_zipcodes = records[records['zipcode'] != 'Total Average']['zipcode'].dropna().astype(str).tolist()
dropdown1 = Dropdown(label="select zipcode1", menu=valid_zipcodes)
dropdown2 = Dropdown(label="select zipcode2", menu=valid_zipcodes)
dropdown1.on_event('menu_item_click', change_1)
dropdown2.on_event('menu_item_click', change_2)


curdoc().add_root(column(dropdown1, dropdown2, p))

