#execute this file to detect moving objects in webcam, press q to quit
#automatically displays times object enters and exits frame in bokeh plot with info in popup
from MotionDetection import df

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource

#convert orig cols to strings so hovertool method can display in popup
#creates new cols Start_string and End_string
df["Start_string"]=df["start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["end"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df) #conv df to cds obj

output_file("MotionGraph.html")
f=figure(width=500,height=100,x_axis_type="datetime",sizing_mode='scale_width',title="Motion Graph")
f.yaxis.minor_tick_line_color=None
f.yaxis.ticker.desired_num_ticks=1

#takes 'tooltips' param which takes list of tuples - start string then array of data
hover=HoverTool(tooltips=[("start","@Start_string"), ("end","@End_string")])
f.add_tools(hover) #add tool

#top and bottom always 1 and 0, pass source param as cds
q=f.quad(left="start",right="end",bottom=0,top=1,color="green", source=cds)

show(f)
