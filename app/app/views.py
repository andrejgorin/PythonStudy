from flask import render_template, flash
from app import app
from vdb import frdb
from jinja2 import Template, Environment, meta
from forms import LoginForm

@app.route("/")
@app.route('/index')

def index():
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    return render_template("index.html",
           results = results)

@app.route('/<vendor>')

def fvendor(vendor):
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    strven = vendor.encode('utf-8')
    resall = frdb("SELECT * FROM device_templates WHERE vendor LIKE '%s'" % strven)
    arg = []
    for resall in resall:
        arg.append(resall[2:5])
    return render_template("ventable.html",
           arg = arg,
           results = results,
           vendor = vendor)

@app.route('/confgen/<query>', methods = ['GET', 'POST'])

def test(query):
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    strquery = query.encode('utf-8')
    temp = frdb("SELECT template FROM device_templates where name LIKE '%s'" % strquery)
    template = temp[0][0]
    temp = template
    env = Environment()
    ast = env.parse(template)
    vars = meta.find_undeclared_variables(ast)
    vars = list(vars)
    form = LoginForm()   
    output = ' '   
    tempresult = ' '
    if form.validate_on_submit():
        output = form.openid.data
        output = output.encode('utf-8')
        output = output.split(';')
        output = dict(zip(vars, output))
        rendit = output
        template = Template(template, trim_blocks=True, lstrip_blocks=True)
        tempresult = template.render(rendit)
    return render_template('template.html',
                           tempresult = tempresult,
                           form = form,
                           output = output,
                           temp = temp,
                           results = results,
                           vars = vars)
