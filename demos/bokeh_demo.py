import random
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Dropdown
from bokeh.layouts import column

t = range(0, 100)
s1 = [_+ random.randint(-10, 10) for _ in t]
s2 = [-_+ random.randint(-10, 10) for _ in t]

def select_stock(event):
	if event.item == 's1':
		ds.data['y'] = s1
	elif event.item == 's2':
		ds.data['y'] = s2
	else:
		raise Exception(f'unknown item: {event.item}')
	ds.trigger('data', ds.data, ds.data)

p = figure(x_range=(min(t), max(t)), y_range=(min(s2), max(s1)), title="Simple stock trends")

p.line(list(t), s1)
menu = [('stock1', 's1'), ('stock2', 's2')]
dropdown = Dropdown(label="select stock", menu=menu)
dropdown.on_event('menu_item_click', select_stock)

curdoc().add_root(column(p, dropdown))

import random
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Dropdown, ColumnDataSource
from bokeh.layouts import column

# Generate synthetic data
t = list(range(0, 100))
s1 = [x + random.randint(-10, 10) for x in t]
s2 = [-x + random.randint(-10, 10) for x in t]

# Create a ColumnDataSource (fixes the missing 'ds' error)
ds = ColumnDataSource(data=dict(x=t, y=s1))

# Fixed indentation and simplified data updating
def select_stock(event):
    if event.item == 's1':
        ds.data = dict(x=t, y=s1)
    elif event.item == 's2':
        ds.data = dict(x=t, y=s2)
    else:
        raise Exception(f'unknown item: {event.item}')

# Set up the figure
p = figure(x_range=(min(t), max(t)), y_range=(min(s2), max(s1)), title="Simple stock trends")

# Point the line to the ColumnDataSource instead of raw lists
p.line('x', 'y', source=ds)

# Set up the dropdown and callback
menu = [('stock1', 's1'), ('stock2', 's2')]
dropdown = Dropdown(label="select stock", menu=menu)
dropdown.on_event('menu_item_click', select_stock)

# Add to the document
curdoc().add_root(column(p, dropdown))