from flask import render_template, request
from app import app
from vdb import frdb
from jinja2 import Template, Environment, meta
from forms import TemForm, DataForm, TempTemplate, TempHeader, TempString

@app.route("/")
@app.route('/index')

def index():
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    return render_template("index.html",
           results = results)

@app.route('/<vendor>', methods = ['GET', 'POST'])

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

@app.route('/confgen/<int:query>', methods = ['GET', 'POST'])

def confgen(query):
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
    tform = DataForm()
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
                           inputform = inputform,
                           stringvars = stringvars,
                           manform = manform,
                           nlines = nlines,
                           stringtem = stringtem,
                           results = results)
                           
@app.route('/combo', methods = ['GET', 'POST'])

def combo():
    results = frdb("SELECT vendor FROM device_templates")
    results = {i[0] for i in results}
    tform = DataForm()
    buffer = TempTemplate()
    headers = TempHeader()
    longstring = TempString()
    template = ''
    i = 0
    paramlist = []
    temp_header_string = ''
    nlines = False
    line_length = False
    temout = []
    tformdata = False
    stringtem = ''
    dicis = []
    header = []
    head = []
    header_string = ''
    line_length = 45
    temp = False
    stringvars = False
    checkbox_value = request.form.getlist('checkbox_list')
    checkbox_value = [value.encode('utf-8') for value in checkbox_value] 
    checkbox_value = map(int, checkbox_value)
    for check in checkbox_value:        
        one_header = frdb("SELECT * FROM device_templates where uid = '%d'" % check)
        header.append(one_header[0][1:4])
    if header:
        for head in header:
            if i == (len(header)) - 1:
                for h in head:
                    header_string = header_string + str(h) + ' '
                header_string = header_string + ' '
            else:
                for h in head:
                    header_string = header_string + str(h) + ' '
                header_string = header_string + '& '
            i += 1
        header_string = header_string + 'configuration'
        headers.header_list.data = header
    if headers.header_list.data:
        temp_header = headers.header_list.data
    if header_string:
        longstring.string_list.data = header_string
    if longstring.string_list.data:
        header_string = longstring.string_list.data
    for check in checkbox_value:
        one_template = frdb("SELECT template FROM device_templates where uid = '%s'" % check)
        one_template = str(one_template[0][0])
        template = template + '\n' + '!'*40 + '\n' + one_template
    if template:
        buffer.temp_template.data = template
    if buffer.temp_template.data:#buffer.validate():
        temp = buffer.temp_template.data
        env = Environment()
        ast = env.parse(buffer.temp_template.data)
        vars = meta.find_undeclared_variables(ast)
        vars = list(vars)
        stringvars = ';'.join(vars)
        temout = []
        if tform.validate():
            tformdata = tform.body.data
            tformdata = tformdata.replace('\r\n', '')
            tformdata = tformdata.encode('utf-8')
            tformdata = tformdata.split('#')
            template = buffer.temp_template.data
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
    return render_template('combo.html', 
                           header_string = header_string,
                           tform = tform,
                           stringvars = stringvars,
                           buffer = buffer,
                           headers = headers,
                           longstring = longstring,
                           temout = temout,
                           nlines = nlines,
                           line_length = line_length,
                           stringtem = stringtem,
                           temp = temp,
                           results = results)