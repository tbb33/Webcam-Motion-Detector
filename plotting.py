#execute this file after MotionDetection.py to displays times object enters and exits frame in Bokeh graph
from bokeh.plotting import figure
from bokeh.io import output_file, show
import pandas

list=[]
i=0
df=pandas.read_csv("MotionTimes.csv",parse_dates=["start","end"])
lft=df["start"]

output_file("Quad.html")
f=figure(width=400,height=400,x_axis_type="datetime")
f.title.text="Motion Graph"
#top and bottom always 1 and 0
while i in range(len(lft)):
    toplist=[1]*len(lft)
    botlist=[0]*len(lft)
    i=i+1

f.quad(top=toplist, bottom=botlist, left=df["start"], right=df["end"])

show(f)
