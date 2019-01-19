import numpy as np
import scipy.special
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import file_html
from bokeh.palettes import Spectra15, Viridis3
from bokeh.transform import factor_cmap
import holoviews as hv
from holoviews import opts
hv.extension("bokeh")

def Run():
    return

def VBar(dfData, xcol, ycol, charttitle, returnObject = False):
    #This is required for the bug in bokeh as it cannot handle category columns
    if(dfData[xcol].dtype.name == "category"):
        dfData[xcol] = dfData[xcol].astype("object")
    xdata = dfData[xcol]
    ydata = dfData[ycol]
    p = figure(x_range=xdata, title=charttitle, toolbar_location=None, tools="")
    p.vbar(x=xdata, top=ydata, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    if(returnObject):
        return p
    else:
        output_file(charttitle + ".html")
        show(p)
    return

#def VBar2(dfData, xgcol1, xgcol2, dimension, charttitle, xtitle, xlabel, objwidth=500, objheight=500, returnObject=False):
#    vbar = hv.Bars(dfData.to_records[index=False].tolist(), [xgcol1, xgcol2], dimension)
#    if(objwidth is not None):
#        vbar.opts(width)
#    return