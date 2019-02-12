import numpy as np
import scipy.special
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import file_html
from bokeh.palettes import Spectral5, Viridis3
from bokeh.transform import factor_cmap
import holoviews as hv
from holoviews import opts
hv.extension("bokeh")

def Run():
    return

def Archive():
    Intro()
    Intro2()
    Intro3()
    Intro4()
    Intro5()
    return

def Intro():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    show(p)
    return

def Intro2():
    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i**2 for i in x]
    y1 = [10**i for i in x]
    y2 = [10**(i**2) for i in x]

    # output to static HTML file
    output_file("log_lines.html")

    # create a new plot
    p = figure(
       tools="pan,box_zoom,reset,save",
       y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
       x_axis_label='sections', y_axis_label='particles'
    )

    # add some renderers
    p.line(x, x, legend="y=x")
    p.circle(x, x, legend="y=x", fill_color="white", size=8)
    p.line(x, y0, legend="y=x^2", line_width=3)
    p.line(x, y1, legend="y=10^x", line_color="red")
    p.circle(x, y1, legend="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

    # show the results
    show(p)

def Intro3():
    # prepare some data
    N = 4000
    x = np.random.random(size=N) * 100
    y = np.random.random(size=N) * 100
    radii = np.random.random(size=N) * 1.5
    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
    ]

    # output to static HTML file (with CDN resources)
    output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")

    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

    # create a new plot with the tools above, and explicit ranges
    p = figure(tools=TOOLS, x_range=(0, 100), y_range=(0, 100))

    # add a circle renderer with vectorized colors and sizes
    p.circle(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

    # show the results
    show(p)

def Intro4():
    # prepare some data
    N = 100
    x = np.linspace(0, 4*np.pi, N)
    y0 = np.sin(x)
    y1 = np.cos(x)
    y2 = np.sin(x) + np.cos(x)

    # output to static HTML file
    output_file("linked_panning.html")

    # create a new plot
    s1 = figure(width=250, plot_height=250, title=None)
    s1.circle(x, y0, size=10, color="navy", alpha=0.5)

    # NEW: create a new plot and share both ranges
    s2 = figure(width=250, height=250, x_range=s1.x_range, y_range=s1.y_range, title=None)
    s2.triangle(x, y1, size=10, color="firebrick", alpha=0.5)

    # NEW: create a new plot and share only one range
    s3 = figure(width=250, height=250, x_range=s1.x_range, title=None)
    s3.square(x, y2, size=10, color="olive", alpha=0.5)

    # NEW: put the subplots in a gridplot
    p = gridplot([[s1, s2, s3]], toolbar_location=None)

    # show the results
    show(p)

def Intro5():
    # prepare some date
    N = 300
    x = np.linspace(0, 4*np.pi, N)
    y0 = np.sin(x)
    y1 = np.cos(x)

    # output to static HTML file
    output_file("linked_brushing.html")

    # NEW: create a column data source for the plots to share
    source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1))

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

    # create a new plot and add a renderer
    left = figure(tools=TOOLS, width=350, height=350, title=None)
    left.circle('x', 'y0', source=source)

    # create another new plot and add a renderer
    right = figure(tools=TOOLS, width=350, height=350, title=None)
    right.circle('x', 'y1', source=source)

    # put the subplots in a gridplot
    p = gridplot([[left, right]])

    # show the results
    show(p)

def IntroGridPlot():
    x = list(range(11))
    y0 = x
    y1 = [10 - i for i in x]
    y2 = [abs(i - 5) for i in x]

    # create three plots
    p1 = figure(plot_width=250, plot_height=250, title=None)
    p1.circle(x, y0, size=10, color=Viridis3[0])
    p2 = figure(plot_width=250, plot_height=250, title=None)
    p2.triangle(x, y1, size=10, color=Viridis3[1])
    p3 = figure(plot_width=250, plot_height=250, title=None)
    p3.square(x, y2, size=10, color=Viridis3[2])
    p4 = figure(plot_width=250, plot_height=250, title=None)
    p4.circle(x, y0, size=10, color=Viridis3[0])
    p5 = figure(plot_width=250, plot_height=250, title=None)
    p5.triangle(x, y1, size=10, color=Viridis3[1])
    
    fileobjects = [p1, p2, p3, p4, p5]
    PlotGrid("grid.html", fileobjects, 2)
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
        output_file(charttitle + " .html")
        show(p)
    return

def VBar2(dfData, xgcol1, xgcol2, dimension, charttitle,xtitle, xlabel, objwidth = 500, objheight = 500, returnObject = False):
    vbar = hv.Bars(dfData.to_records(index=False).tolist(), [xgcol1, xgcol2], dimension)
    if(objwidth is not None):
        vbar.opts(width = objwidth)
    if(objheight is not None):
        vbar.opts(height = objheight)
    stacked = vbar.opts(stacked=True, clone=True)
    vbar.relabel(group='Grouped') + stacked.relabel(group='Stacked')
    renderer = hv.renderer('bokeh')
    # Convert to bokeh figure then save using bokeh
    plot = renderer.get_plot(vbar).state
    if(returnObject):
        return plot
    else:
        output_file(charttitle + ".html")
        show(plot)
    return

def VBar2Stacked(dfData, xgcol1, xgcol2, dimension, charttitle,xtitle, xlabel, objwidth = 500, objheight = 500, returnObject = False):
    vbar = hv.Bars(dfData.to_records(index=False).tolist(), [xgcol1, xgcol2], dimension)
    if(objwidth is not None):
        vbar.opts(width = objwidth)
    if(objheight is not None):
        vbar.opts(height = objheight)
    stacked = vbar.opts(stacked=True)
    vbar.relabel(group='Grouped') + stacked.relabel(group='Stacked')
    #stacked
    stacked = vbar.opts(stacked = True, clone = True)
    stacked.relabel(group = "Stacked")
    renderer = hv.renderer('bokeh')
    # Convert to bokeh figure then save using bokeh
    plot = renderer.get_plot(stacked).state
    if(returnObject):
        return plot
    else:
        output_file(charttitle + "stacked.html")
        show(plot)
    return

def DataFrameToTable(dfData, tableName, returnObject = False):
    Columns = [TableColumn(field=Ci, title=Ci) for Ci in dfData.columns] # bokeh columns
    data_table = DataTable(columns=Columns, source=ColumnDataSource(dfData)) # bokeh table
    if(returnObject):
        return data_table
    else:
        # output to static HTML file
        output_file(tableName + ".html")
        show(data_table)
    return

def SaveHTMLtoFile(file, fileName):
    with open("/"+fileName) as f:
        f.write(file)

def PlotGrid(filename, fileobjects, maxRowObjects):
    # make a grid
    gridlist = []
    rowlist = []
    rownum = 0
    for fileobject in fileobjects:
        if(rownum >= maxRowObjects):
            gridlist.append(rowlist)
            rowlist = []
            rownum = 0
        else:
            rowlist.append(fileobject)
            rownum = rownum + 1
    
    gridlist.append(rowlist)
    grid = gridplot(gridlist)
    # show the results
    output_file(filename)
    show(grid)
    return

def PlotObjects(filename, fileobjects):
    output_file(filename)
    show(column(fileobjects))
    return