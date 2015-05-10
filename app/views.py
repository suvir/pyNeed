from app import app
from flask import render_template, flash, request, url_for, redirect, session, Response, jsonify
from forms import SignupForm, LoginForm, ProductAddForm, DealForm, EditProfileForm
from models import Vendor
from utility_funcs import get_password_hash, check_password, parse_product_catalog_multidict, parse_deal_list_multidict, get_coordinates
from ast import literal_eval
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
        if vendor is None:
            prod_count = str(len(vendor.product_catalog))
            vendor_deal_count = str(len(vendor.deal_list))
            return render_template('index.html', form='null', v=vendor, products=vendor.product_catalog, product_count=prod_count, deal_count = vendor_deal_count, email=session['email'], loginform=loginform)
        else:
            return redirect(url_for('login'))           

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
    return render_template('index.html', form=form, email='', loginform=loginform, v='')


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


@app.route('/deals', methods=['GET', 'POST', 'DELETE'])
def deals():
    form = DealForm(request.form)

    # Authentication Guard 1
    if 'email' not in session:
        return redirect(url_for('login'))

    # Authentication Guard 2
    if 'email' in session:
        vendors_with_email = Vendor.objects(email=session['email'])
        vendor = vendors_with_email.first()

    # Received a form
    if request.method == 'POST':
        print(request.form)
        if request.form['editremove'].split("#")[0] == 'Remove':
            print "INSIDE REMOVE"
            f = request.form
            deal_name =request.form['editremove'].split("#")[1]
            product_name = request.form['editremove'].split("#")[2]
            description = request.form['editremove'].split("#")[3]
            price = request.form['editremove'].split("#")[4]
            vendors_with_email = Vendor.objects(email=session['email'])
            vendor = vendors_with_email.first()

            print product_name
            
            for deal in vendor.deal_list:
                if deal.name == deal_name and product_name == deal.product_name:
                    print "INSIDE IF FOR DEAL"
                    vendor.deal_list.remove(deal)

            vendor.save()

        elif request.form['editremove'].split("#")[0] == 'Edit':
            print "Editing"

        elif request.form['editremove'] == 'Add Deal':
            vendors_with_email = Vendor.objects(email=session['email'])
            print "Inside adding deals.."
            f = request.form

            deals = parse_deal_list_multidict(f)
            print deals

            # Find the vendor in database with matching email address

            if len(vendors_with_email) > 1:
                print "Error : Multiple vendors in database with same email"
            vendor = vendors_with_email.first()
            vendor.deal_list.extend(deals)
            vendor.save()
            flash("Added deals to database")

        else:
            print "Not inside any form..."

    return render_template('deals.html', loginform='', email=session['email'], vendor=vendor, deals=vendor.deal_list)

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

    return render_template('signup.html', form=form,email='')


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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = EditProfileForm()

    if 'email' not in session:
        return redirect(url_for('login'))

    # Find the vendor in database with matching email address
    vendors_with_email = Vendor.objects(email=session['email'])
    if len(vendors_with_email) > 1:
        print "Error : Multiple vendors in database with same email"

    vendor = vendors_with_email.first()
    prod_count = str(len(vendor.product_catalog))
    vendor_deal_count = str(len(vendor.deal_list))

    if form.validate_on_submit():
        flash('Profile Edited')
        print "Successfully validated profile edit form!!"
        coords = get_coordinates(form.address.data+" "+form.city.data)
        vendor.name=form.name.data
        vendor.description=form.description.data
        vendor.email=form.email.data
        vendor.category=form.category.data
        vendor.address=form.address.data
        vendor.phone=form.phone.data
        vendor.state=form.state.data
        vendor.city=form.city.data
        vendor.latitude=repr(coords[0])
        vendor.longitude=repr(coords[1])
        print "New city",form.city.data
        vendor.save()
        print "Finished updating profile"
    else:
        form.name.data = vendor.name
        form.description.data = vendor.description
        form.email.data = vendor.email
        form.category.data = vendor.category
        form.phone.data = vendor.phone
        form.address.data = vendor.address
        print "Vendor category", form.category.choices, form.category.data
        print "Vendor form city", vendor.city
        form.city.data = vendor.city
        form.state.data = vendor.state


    if vendor is None:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html', v=vendor, products=vendor.product_catalog, deals = vendor.deal_list, product_count=prod_count, deal_count = vendor_deal_count, form=form)


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

@app.route('/api/vendor/types', methods=['GET'])
def getallvendortypes():
    result = []
    types_returned = []
    with open('vendor_types', 'r') as f:
        for line in f:
            result.append(literal_eval(line.strip()))


    for type in result[0]:
        print type
        types={}
        types['type']=type[1]
        types_returned.append(types)


    resp = jsonify({'vendor_types':types_returned})
    resp.status_code = 200
    return resp

@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))