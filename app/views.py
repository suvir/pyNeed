from app import app
from flask import render_template, flash, request, url_for, redirect, session, Response, jsonify
from forms import SignupForm, LoginForm, ProductAddForm, EditProfileForm
from models import Vendor
from utility_funcs import get_password_hash, check_password, parse_product_catalog_multidict, get_coordinates
import bson


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignupForm(request.form)
    loginform = LoginForm()

    if 'email' in session:
         # Find the vendor in database with matching email address
        vendors_with_email = Vendor.objects(email=session['email'])
        if len(vendors_with_email) > 1:
            print "Error : Multiple vendors in database with same email"

        vendor = vendors_with_email.first()
        prod_count = str(len(vendor.product_catalog))
        return render_template('index.html', form='null', v = vendor, products=vendor.product_catalog, product_count=prod_count, email=session['email'], loginform=loginform)

    if request.method == 'POST' and form.validate():
        flash('Signup requested')
        print "Successfully validated form!!"
        print "name received", form.name, 'data:', form.name.data
        # Hash the password and save to database
        pwdhash = get_password_hash(form.password.data)
        coords = get_coordinates(form.address.data+" "+form.city.data)
        print coords[0]
        print coords[1]
        new_vendor = Vendor(name=form.name.data, description=form.description.data, email=form.email.data,
                            category=form.category.data, address=form.address.data, phone=form.phone.data,
                            state=form.state.data, city=form.city.data, pwdhash=pwdhash, latitude=repr(coords[0]), longitude=repr(coords[1]))
        new_vendor.save()
        # Add email to cookie
        session['email'] = new_vendor.email
        return redirect(url_for('index'))

    if request.method == 'POST' and loginform.validate():
        vendors_with_email = Vendor.objects(email=loginform.email.data)
        if len(vendors_with_email) > 1:
            print "Error : Multiple vendors in database with same email"

        vendor = vendors_with_email.first()

        # First check that a vendor with this email address exists in database
        if vendor is None:
            flash('No vendor in database with this email address')
            loginform.email.errors.append("Unknown email address")
            flash('Login failed because no vendor found')

        # Since vendor exists in database, check that the correct password was supplied
        if vendor is not None and check_password(vendor.pwdhash, form.password.data):
            flash('Login successful')
            print "Logged in successfully"
            session['email'] = loginform.email.data
            return redirect(url_for('index'))
        else:
            loginform.password.errors.append("Incorrect password")
            flash('Login failed because incorrect password')

    print(loginform.errors)
    return render_template('index.html', form=form, email='', loginform=loginform, v = '')


@app.route('/catalog', methods=['GET', 'POST', 'DELETE'])
def catalog():
    form = ProductAddForm(request.form)
    if 'email' not in session:
        return redirect(url_for('login'))

    if 'email' in session:
        vendors_with_email = Vendor.objects(email=session['email'])
        vendor = vendors_with_email.first()

    if request.method == 'POST':
        print(request.form)
        if request.form['editremove'].split("#")[0] == 'Remove':
            print "INSIDE REMOVE"
            f = request.form
            product_name =request.form['editremove'].split("#")[1]
            product_description = request.form['editremove'].split("#")[2]
            vendors_with_email = Vendor.objects(email=session['email'])
            vendor = vendors_with_email.first()

            print product_name
            for product in vendor.product_catalog:

                if product.name == product_name and product.description == product_description:
                    print"INSIDE IF"
                    vendor.product_catalog.remove(product)
                    break

            vendor.save()

        elif request.form['editremove'].split("#")[0] == 'Edit':
            print "Editing"

        elif request.form['editremove'] == 'Add Product':
            vendors_with_email = Vendor.objects(email=session['email'])
            print "Inside ADD:.."
            f = request.form

            products = parse_product_catalog_multidict(f)
            print products

            # Find the vendor in database with matching email address

            if len(vendors_with_email) > 1:
                print "Error : Multiple vendors in database with same email"
            vendor = vendors_with_email.first()
            vendor.product_catalog.extend(products)
            vendor.save()
            flash("Added products to database")



        else:
            print "Not inside any form..."

    return render_template('product_catalog.html', loginform='', email=session['email'], vendor=vendor,
                           products=vendor.product_catalog)

######### Signup not in use #############
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
        return redirect(url_for('index'))

    return render_template('signup.html', form=form,email=email)


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
            return redirect(url_for('index'))
        else:
            form.password.errors.append("Incorrect password")
            flash('Login failed because incorrect password')

    return render_template('login.html', form=form)




@app.route('/api/vendor/type/<vendorid>', methods=['GET'])
def getvendortype(vendorid):
    if bson.ObjectId.is_valid(vendorid):
        vendors = Vendor.objects(id=vendorid)
        if len(vendors)>=1:
            resp = jsonify({'vendor_type':vendors.first().category})
            resp.status_code = 200
            return resp
    else:
        message={
            'status':404,
            'message': 'Not found, vendor with id:'+vendorid
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))