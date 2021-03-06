from app import app
from flask import render_template, flash, request, url_for, redirect, session, jsonify
from ast import literal_eval
import bson

from Forms import SignupForm, LoginForm, ProductAddForm, DealForm, EditProfileForm
from Models import VendorManager, ProductManager, DealManager, TransactionManager


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignupForm(request.form)
    loginform = LoginForm()

    if 'email' in session:
        # Find the vendor in database with matching email address
        vendor_id, vendor = VendorManager.get_vendor(email=session['email'])
        if vendor is not None:
            prod_count = str(len(vendor.product_catalog))
            vendor_deal_count = str(len(vendor.deal_list))
            return render_template('index.html', form='null', v=vendor, products=vendor.product_catalog,
                                   product_count=prod_count, deal_count=vendor_deal_count, email=session['email'],
                                   loginform=loginform)
        else:
            return redirect(url_for('login'))

    if request.method == 'POST' and request.form['submit'] == "Register" and form.validate_on_submit():
        flash('Signup requested')
        print "Successfully validated form!!"
        print "name received", form.name, 'data:', form.name.data
        # Hash the password and save to database
        pwdhash = VendorManager.get_password_hash(form.password.data)
        coords = VendorManager.get_vendor_coordinate(form.address.data + " " + form.city.data)
        print coords[0]
        print coords[1]
        given_data = {}
        given_data['name'] = form.name.data
        given_data['description'] = form.description.data,
        given_data['email'] = form.email.data
        given_data['type'] = form.category.data
        given_data['address'] = form.address.data
        given_data['phoneNumber'] = form.phone.data
        given_data['state'] = form.state.data
        given_data['city'] = form.city.data
        given_data['password'] = pwdhash
        given_data['coordinates'] = [repr(coords[0]), repr(coords[1])]

        new_vendor = VendorManager.create_vendor(given_data)
        print "CHECKING IF VENDOR W/ EMAIL EXISTS"
        print VendorManager.get_vendor(email=form.email.data)
        if VendorManager.get_vendor(email=form.email.data) is None:
            VendorManager.post_vendor(new_vendor)
            # Add email to cookie
            session['email'] = new_vendor.email
            return redirect(url_for('profile'))
        else:
            form.email.errors.append("User with email: " + request.form['email'] + " already exists in the database")
            flash("Enrollment failed")
            return render_template('index.html', form=form, email='', loginform=loginform, v='')

    elif request.method == 'POST' and request.form['submit'] == "Login" and loginform.validate_on_submit():
        vid, vendor = VendorManager.get_vendor(email=loginform.email.data)

        # First check that a vendor with this email address exists in database
        if vendor is None:
            flash('No vendor in database with this email address')
            loginform.email.errors.append("Unknown email address")
            flash('Login failed because no vendor found')

        # Since vendor exists in database, check that the correct password was supplied
        if vendor is not None and VendorManager.check_password(vendor.pwdhash, form.password.data):
            flash('Login successful')
            print "Logged in successfully"
            session['email'] = loginform.email.data
            return redirect(url_for('profile'))
        else:
            loginform.password.errors.append("Incorrect password")
            flash('Login failed because incorrect password')

    # print "Form errors below:"
    # print(form.errors)
    return render_template('index.html', form=form, email='', loginform=loginform, v='')


@app.route('/catalog', methods=['GET', 'POST', 'DELETE'])
def catalog():
    form = ProductAddForm(request.form)
    if 'email' not in session:
        return redirect(url_for('index'))
    else:
        vid, vendor = VendorManager.get_vendor(email=session['email'])
        if vendor is None:
            print "No such vendor in database"
        else:
            prod_count = str(len(vendor.product_catalog))
            vendor_deal_count = str(len(vendor.deal_list))

    if request.method == 'POST':
        print(request.form)
        if request.form['editremove'].split("#")[0] == 'Remove':
            print "INSIDE REMOVE"
            f = request.form
            product_name = request.form['editremove'].split("#")[1]
            product_description = request.form['editremove'].split("#")[2]
            vid, vendor = VendorManager.get_vendor(email=session['email'])

            print product_name
            for product in vendor.product_catalog:

                if product.name == product_name and product.description == product_description:
                    print"INSIDE IF"
                    vendor.product_catalog.remove(product)
                    ProductManager.delete_product(vid, product)
                    break

        elif request.form['editremove'].split("#")[0] == 'Edit':
            print "Editing"

        elif request.form['editremove'] == 'Add Product':
            print "Inside ADD:.."
            f = request.form

            products = ProductManager.parse_product_catalog_multidict(f)
            print products

            # Find the vendor in database with matching email address
            vid, vendor = VendorManager.get_vendor(email=session['email'])
            vendor.product_catalog.extend(products)

            for prod in products:
                ProductManager.post_product(prod, vid)
            flash("Added products to database")

        else:
            print "Not inside any form..."

    return render_template('product_catalog.html', loginform='', email=session['email'], vendor=vendor,
                           products=vendor.product_catalog, product_count=prod_count, deal_count=vendor_deal_count)


@app.route('/deals', methods=['GET', 'POST', 'DELETE'])
def deals():
    form = DealForm(request.form)

    # Authentication Guard 1
    if 'email' not in session:
        return redirect(url_for('index'))
    else:
        # Authentication Guard 2
        vid, vendor = VendorManager.get_vendor(email=session['email'])
        if vendor is None:
            print "No such vendor in database"
        else:
            prod_count = str(len(vendor.product_catalog))
            vendor_deal_count = str(len(vendor.deal_list))


    # Received a form
    if request.method == 'POST':
        print(request.form)
        if request.form['editremove'].split("#")[0] == 'Remove':
            print "INSIDE REMOVE DEALS"
            f = request.form
            deal_id = request.form['deal_id']

            deal_name = request.form['editremove'].split("#")[1]
            product_name = request.form['editremove'].split("#")[2]
            description = request.form['editremove'].split("#")[3]
            price = request.form['editremove'].split("#")[4]

            print product_name

            for deal in vendor.deal_list:
                if deal.id == deal_id:
                    print "INSIDE IF FOR DEAL"
                    vendor.deal_list.remove(deal)
                    DealManager.delete_deal(vid, deal, vendor.name)

        elif request.form['editremove'].split("#")[0] == 'Edit':
            print "Editing"

        elif request.form['editremove'] == 'Add Deal':
            vid, vendor = VendorManager.get_vendor(email=session['email'])
            print "Inside adding deals.."
            f = request.form

            deals = DealManager.parse_deal_list_multidict(f)
            print deals

            # Find the vendor in database with matching email address
            vendor.deal_list.extend(deals)
            for deal in deals:
                DealManager.post_deal(deal, vendor.name, vid)
            flash("Added deals to database")

        else:
            print "Not inside any form..."

    return render_template('deals.html', loginform='', email=session['email'], vendor=vendor, deals=vendor.deal_list,
                           products=vendor.product_catalog, product_count=prod_count, deal_count=vendor_deal_count)


@app.route('/transactions')
def transactions():
    if 'email' not in session:
        return redirect(url_for('index'))
    else:
        # Find the vendor in database with matching email address
        vid, vendor = VendorManager.get_vendor(email=session['email'])

        transaction_list = TransactionManager.get_all_transactions_for_vendor(session['email'])
        prod_count = str(len(vendor.product_catalog))
        vendor_deal_count = str(len(vendor.deal_list))
        return render_template('transactions.html', loginform='', email=session['email'], transactions=transaction_list, product_count=prod_count, deal_count=vendor_deal_count)


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
        pwdhash = VendorManager.get_password_hash(form.password.data)

        new_vendor = VendorManager.create_vendor(name=form.name.data, description=form.description.data,
                                                 email=form.email.data,
                                                 category=form.category.data, address=form.address.data,
                                                 phone=form.phone.data,
                                                 state=form.state.data, city=form.city.data, pwdhash=pwdhash)
        VendorManager.post_vendor(new_vendor)
        # Add email to cookie
        session['email'] = new_vendor.email
        return redirect(url_for('profile'))

    return render_template('signup.html', form=form, email='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if form.validate_on_submit():
        vid, vendor = VendorManager.get_vendor(email=form.email.data)

        # First check that a vendor with this email address exists in database
        if vendor is None:
            flash('No vendor in database with this email address')
            form.email.errors.append("Unknown email address")
            flash('Login failed because no vendor found')

        # Since vendor exists in database, check that the correct password was supplied
        if vendor is not None and VendorManager.check_password(vendor.pwdhash, form.password.data):
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
    vid, vendor = VendorManager.get_vendor(email=session['email'])

    prod_count = str(len(vendor.product_catalog))
    vendor_deal_count = str(len(vendor.deal_list))

    if form.validate_on_submit():
        flash('Profile Edited')
        print "Successfully validated profile edit form!!"
        coords = VendorManager.get_vendor_coordinate(form.address.data + " " + form.city.data)
        vendor.name = form.name.data
        vendor.description = form.description.data
        vendor.email = form.email.data
        vendor.category = form.category.data
        vendor.address = form.address.data
        vendor.phone = form.phone.data
        vendor.state = form.state.data
        vendor.city = form.city.data
        vendor.latitude = repr(coords[0])
        vendor.longitude = repr(coords[1])
        print "New city", form.city.data
        VendorManager.put_vendor(vendor)
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
        return render_template('profile.html', email=session['email'], v=vendor, products=vendor.product_catalog,
                               deals=vendor.deal_list, product_count=prod_count, deal_count=vendor_deal_count,
                               form=form, loginform='')


# Service that gets vendor type for a specific vendorid
@app.route('/api/vendor/type/<vendorid>', methods=['GET'])
def getvendortype(vendorid):
    if bson.ObjectId.is_valid(vendorid):
        vendors = VendorManager.get_vendor(vendor_id=vendorid)
        if vendors is not None:
            resp = jsonify({'vendor_type': vendors.category})
            resp.status_code = 200
            return resp
        else:
            message = {
                'status': 404,
                'message': 'Not found, vendor with id:' + vendorid
            }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
    else:
        message = {
            'status': 404,
            'message': 'Not found, vendor with id:' + vendorid
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp


# Service that gets all vendor types
@app.route('/api/vendor/types', methods=['GET'])
def getallvendortypes():
    result = []
    types_returned = []
    with open('vendor_types', 'r') as f:
        for line in f:
            result.append(literal_eval(line.strip()))

    for vendor_type in result[0]:
        print type
        vendor_types = {}
        vendor_types['type'] = vendor_type[1]
        types_returned.append(vendor_types)

    resp = jsonify({'vendor_types': types_returned})
    resp.status_code = 200
    return resp


# Service that returns a product catalog for a specific vendorid
@app.route('/api/vendor/catalog/<vendorid>', methods=['GET'])
def getvendorcatalog(vendorid):
    if bson.ObjectId.is_valid(vendorid):
        vendor = VendorManager.get_vendor(vendor_id=vendorid)
        if vendor is not None:
            print "found matching vendors"
            products = []
            for product in vendor.product_catalog:
                p = {}
                p['id'] = str(product.id)
                p['name'] = product.name
                p['description'] = product.description
                p['price'] = product.price
                products.append(p)
            resp = jsonify({'products': products})
            resp.status_code = 200
            return resp
        else:
            message = {
                'status': 404,
                'message': 'Not found, vendor with id:' + vendorid
            }
            resp = jsonify(message)
            resp.status_code = 404
            return resp
    else:
        message = {
            'status': 404,
            'message': 'Not found, vendor with id:' + vendorid
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp


# Service that returns a list of all vendors
@app.route('/api/vendors/', methods=['GET'])
def get_all_vendors():
    vendors = VendorManager.get_all_vendors()
    resp = jsonify({'vendors': vendors})
    resp.status_code = 200
    return resp


# Service that notifies Vendors when a transaction is made
@app.route('/api/vendor/notify', methods=['GET'])
def notifyAllVendors():
    if bson.ObjectId.is_valid(request.args.get('vendorId')):
        vendor = VendorManager.get_vendor(vendor_id=request.args.get('vendorId'))
        if vendor is not None:
            VendorManager.email_vendor(vendor.email,request.args.get('message'),request.args.get('transactionId'))
            resp = jsonify({'message': "Vendor with id: " + request.args.get('vendorId') + " successfully notified"})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify(
                {'message': "Vendor id: " + request.args.get('vendorId') + " Does not exist in the database"})
            resp.status_code = 404
            return resp

    else:
        resp = jsonify({'message': "Vendor id: " + request.args.get('vendorId') + " is invalid"})
        resp.status_code = 404
        return resp


@app.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('login'))

    session.pop('email', None)
    return redirect(url_for('index'))
