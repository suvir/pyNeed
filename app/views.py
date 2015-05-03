from app import app
from flask import render_template, flash, request, url_for, redirect, session
from forms import SignupForm, LoginForm
from models import Vendor


@app.route('/')
@app.route('/index')
def index():
    vendor = {'name': 'Suvir'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', vendor=vendor, posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if form.validate_on_submit():
        flash('Signup requested')
        print "Successfully validated form!!"
        new_vendor = Vendor(form.name, form.description, form.email, form.category, form.address, form.phone,
                            form.state, form.city)
        new_vendor.do_something()
        session['email'] = new_vendor.email.data
        return redirect(url_for('profile'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if form.validate_on_submit():
        flash('Login successful')
        print "Logged in successfully"
        session['email'] = form.email.data
        return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('index'))

    return render_template('profile.html')


@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))