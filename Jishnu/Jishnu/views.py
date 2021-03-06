from datetime import datetime
from flask import render_template
from Jishnu import app
import PyBasics
import W1
import W2
import W3
import W4
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

@app.route('/Basics/<id>')
def Basics(id):
    PyBasics.Process(id)
    return render_template(
        'Basics.html',
        dfInfos = PyBasics.dfInfos,
        dfTables = PyBasics.dfTables,
        graphs = PyBasics.graphs,
        notifications = PyBasics.notifications
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

@app.route('/IBMWeek3/<id>')
def IBMWeek3(id):
    W3.ProcessAutosData(id)
    return render_template(
        'IBMWeek3.html',
        dfInfos = W3.dfInfos,
        dfTables = W3.dfTables,
        graphs = W3.graphs,
        notifications = W3.notifications
    )

@app.route('/IBMWeek4/<id>')
def IBMWeek4(id):
    W4.ProcessAutosData(id)
    return render_template(
        'IBMWeek4.html',
        dfInfos = W4.dfInfos,
        dfTables = W4.dfTables,
        graphs = W4.graphs,
        notifications = W4.notifications
    )
