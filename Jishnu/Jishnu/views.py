"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Jishnu import app
import W1
import W2
import X

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/Bootstrap')
def Bootstrap():
    return render_template(
        'Bootstrap.html'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/IBMWeek1')
def IBMWeek1():
    W1.ProcessAutosData()
    return render_template(
        'IBMWeek1.html',
        dfWithHeaders = W1.dfWithHeaders.to_html(header="true", classes="table table-striped table-bordered table-condensed table-responsive", index = False)
    )

@app.route('/IBMWeek2/<id>')
def IBMWeek2(id):
    W2.ProcessAutosData(id)
    return render_template(
        'IBMWeek2.html',
        dfTables = W2.dfTables
    )

@app.route('/IBMWeek3')
def IBMWeek3():
    #W2.ProcessAutosData()
    #dfTables = []
    #for df in W2.dfList:
     #   dfTables.append(df.to_html(header="true", classes="table table-striped table-bordered table-condensed table-responsive", index = False))

    return render_template(
        'IBMWeek3.html',
        #dfList = W2.dfList
        #dfTables = dfTables
    )

@app.route('/IBMWeek4')
def IBMWeek4():
    #W2.ProcessAutosData()
    #dfTables = []
    #for df in W2.dfList:
     #   dfTables.append(df.to_html(header="true", classes="table table-striped table-bordered table-condensed table-responsive", index = False))

    return render_template(
        'IBMWeek2.html',
       # dfList = W2.dfList
        #dfTables = dfTables
    )