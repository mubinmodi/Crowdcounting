from flask import Blueprint, render_template, request, flash, redirect, session, jsonify
# from ..Models.user import User
from Database.mongodb import mongo
from werkzeug.security import generate_password_hash, check_password_hash

import uuid


auth = Blueprint('auth', __name__)


@auth.route('login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        user = mongo.db.users
        email = data.get('email')
        password = data.get('password')

        details = user.find_one({"email": email})

        present = False

        if details != None:
            present = True
        else:
            present = False

        if present:
            if not check_password_hash(details['password'], password):
                flash('Invalid Password',
                      category='error')
            else:

                session['logged_in'] = True
                del details['password']

                details['name'] = details['firstName'] + \
                    " " + details['lastName']

                del details['firstName']
                del details['lastName']
                session['logged_in'] = True
                session['user'] = details
                print(details)

                return redirect('/')
        else:
            flash('We dont have any registered user with this email ID.',
                  category='error')

    return render_template("Auth/Login.html",   details={
        "pageTitle": "Login"
    })


@auth.route('/logout')
# @login_required
def logout():
    # logout_user()
    session.pop('user', None)
    session['logged_in'] = False
    return redirect('/login')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = mongo.db.users
        email = request.form.get('email')
        mobile = int(request.form.get('mobile'))
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')

        print(email, mobile, firstName, lastName, password)

        new_user = {'_id': str(uuid.uuid4()), 'email': email, 'password': generate_password_hash(password, method='sha256'),
                    'firstName': firstName, 'lastName': lastName, 'mobile': mobile, 'control': "Power"
                    }

        user.insert_one(new_user)
        flash('Account Created', category='success')
        return redirect('/login')

    return render_template('Auth/SignUp.html', details={
        "pageTitle": "Signup"
    })

# Password must contain atleast one uppercase letter , one
   # lowercase letter, one number, one special character, length
  #  between 7 - 15 charcters and no white space
