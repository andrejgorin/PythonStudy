from flask_blog import app
from flask import render_template, redirect, url_for
from author.form import RegisterForm

@app.route('/login')
def login():
    return "Hello"
    
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()  
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)    
    
@app.route('/success')
def success():
    return 'Author register'