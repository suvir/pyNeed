from app import app
from flask import render_template, flash, request, url_for, redirect, session
from forms import SignupForm, LoginForm
from models import Vendor
from utility_funcs import get_password_hash, check_password


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
        print "name received", form.name, 'data:', form.name.data
        # Hash the password and save to database
        pwdhash = get_password_hash(form.password.data)
        new_vendor = Vendor(name=form.name.data, description=form.description.data, email=form.email.data,
                            category=form.category.data, address=form.address.data, phone=form.phone.data,
                            state=form.state.data, city=form.city.data, pwdhash=pwdhash)
        new_vendor.save()
        # Add email to cookie
        session['email'] = new_vendor.email
        return redirect(url_for('profile'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if form.validate_on_submit():
        vendors_with_email = Vendor.objects(email=form.email.data)
        if len(vendors_with_email) > 1:
            print "Error : Multiple vendors in database with same email"

        vendor = vendors_with_email.first()

        # First check that a vendor with this email address exists in database
        if vendor is None:
            flash('No vendor in database with this email address')
            form.email.errors.append("Unknown email address")
            flash('Login failed because no vendor found')

        # Since vendor exists in database, check that the correct password was supplied
        if vendor is not None and check_password(vendor.pwdhash, form.password.data):
            flash('Login successful')
            print "Logged in successfully"
            session['email'] = form.email.data
            return redirect(url_for('profile'))
        else:
            form.password.errors.append("Incorrect password")
            flash('Login failed because incorrect password')

    return render_template('login.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))

    # Find the vendor in database with matching email address
    vendors_with_email = Vendor.objects(email=session['email'])
    if len(vendors_with_email) > 1:
        print "Error : Multiple vendors in database with same email"

    vendor = vendors_with_email.first()

    if vendor is None:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html')


@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))