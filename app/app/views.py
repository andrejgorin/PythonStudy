from flask import render_template
from app import app
from vdb import frdb
from jinja2 import Template, Environment, meta
from forms import TemForm, ContactForm#, InputForm

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
#    strven = vendor.encode('utf-8')
    strven = vendor
    resall = frdb("SELECT * FROM device_templates WHERE vendor LIKE '%s'" % strven)
    arg = []
    for resall in resall:
        arg.append(resall[:5])
    return render_template("ventable.html",
           arg = arg,
           results = results,
           vendor = vendor)

@app.route('/confgen/<query>', methods = ['GET', 'POST'])

def test(query):
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    strquery = query
    temp = frdb("SELECT template FROM device_templates where uid = '%s'" % strquery)
    header = frdb("SELECT * FROM device_templates where uid = '%s'" % strquery)
    template = temp[0][0]
    temp = template
    env = Environment()
    ast = env.parse(template)
    vars = meta.find_undeclared_variables(ast)
    vars = list(vars)
    stringvars = ';'.join(vars)
    tform = ContactForm()
    tformdata = []
    output = ' '   
    tempresult = False
    nlines = False
    stringtem = ''
    paramlist = []
    dicis = []
    temout = []
    #if tform.validate_on_submit():
    line_length = 45
    if tform.validate():
        tformdata = tform.body.data
        tformdata = tformdata.replace('\r\n', '')
        tformdata = tformdata.encode('utf-8')
        tformdata = tformdata.split('#')
        template = Template(template, trim_blocks=True, lstrip_blocks=True)
        for single in tformdata:
            paramlist.append(single.split(';'))
        for singleparam in paramlist:
            dicis.append(dict(zip(vars, singleparam))) 
        for dic in dicis:
            temout.append(template.render(dic))
        stringtem = '\n\n'.join(temout)
        nlines = stringtem.count('\n') + 4       
        for lines in stringtem.split('\n'):
            if line_length < len(lines):
                line_length = len(lines)
    return render_template('template.html',
                           temout = temout,
						   tform = tform,
						   tformdata = tformdata,
                           output = output,
                           temp = temp,
                           results = results,
                           vars = vars,
                           stringvars = stringvars,
                           nlines = nlines,
                           line_length = line_length,
                           stringtem = stringtem,
                           header = header)
                           
@app.route('/manual', methods = ['GET', 'POST'])

def manual():
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    #manform = InputForm()
    manform = TemForm()
    inputform = TemForm()
    template = ''
    inputtemplate = False
    line_length = 45
    stringtem = ''
    paramlist = []
    dicis = []
    temout = []
    stringvars = ''
    nlines = False
    if manform.validate():

        inputtemplate = manform.input.data
        inputtemplate = inputtemplate.replace('\r\n', '')
        inputtemplate = inputtemplate.encode('utf-8')
        inputtemplate = inputtemplate.split('#')
        template = inputform.mantemp.data
        template = template.encode('utf-8')
        env = Environment()
        ast = env.parse(template)
        vars = meta.find_undeclared_variables(ast)
        vars = list(vars)
        stringvars = ';'.join(vars)
        template = Template(template, trim_blocks=True, lstrip_blocks=True)

        for single in inputtemplate:
            paramlist.append(single.split(';'))
        for singleparam in paramlist:
            dicis.append(dict(zip(vars, singleparam))) 
        for dic in dicis:
            temout.append(template.render(dic))
        #stringtem = False
        if inputtemplate != ['']:
            stringtem = '\n\n'.join(temout)
        nlines = stringtem.count('\n') + 4       
        for lines in stringtem.split('\n'):
            if line_length < len(lines):
                line_length = len(lines)
    return render_template('manual.html',
                           manform = manform,
                           results = results,
                           inputtemplate = inputtemplate,
                           template = template,
                           inputform = inputform,
                           temout = temout,
                           stringvars = stringvars,
                           stringtem = stringtem,
                           nlines = nlines,
                           line_length = line_length)