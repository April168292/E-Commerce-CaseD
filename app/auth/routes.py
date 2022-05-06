from app.models import db
from flask import Blueprint, render_template, redirect, request, url_for
# import forms and models
from .forms import LoginForm, UserCreationForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# import automated mail dependecies
from flask_mail import Message, Mail
mail = Mail()

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/login', methods=["GET", "POST"])
def logMEin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        print("hi")
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            # check if user exists
            user = User.query.filter_by(username=username).first()

            if user is None or check_password_hash(user.password, password):
                redirect(url_for('auth.logMEin'))
            # log them in
            login_user(user, remember=remember_me)
            return redirect(url_for('FindHome'))

    return render_template('login.html', form=form)


@auth.route('/signup', methods=["GET", "POST"])
def signMEup():
    form = UserCreationForm()
    if request.method == "POST":

        username = form.username.data
        email = form.email.data
        password = form.password.data
        conf = form.confirm_password.data

        print(username, email, password, conf)
        print(form)
        print('post req made')
        if form.validate():
            print('form validated')
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # create an instance of our user
            user = User(username, email, password)

            # add instance to database
            db.session.add(user)
            # commit to database
            db.session.commit()
            return redirect(url_for('auth.logMEin'))
        else:
            print('did not validate')

    return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logMEout():
    logout_user()
    return redirect(url_for('auth.logMEin'))

#
#
# API ROUTES
#
#


@auth.route('/api/signup', methods=["POST"])
def apiSignMeUp():
    data = request.json
    print(data)

    username = data['username']
    email = data['email']
    password1 = data['password1']
    password2 = data['password2']

    if password1 != password2:
        return {
            'status': 'not ok',
            'message': 'The passwords do not match. Try again.'
        }

    # check if user exists
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'A user with that username already exists. Tough.'
        }
    # create an instance of our user
    user = User(username, email, password1)

    # add instance to database
    db.session.add(user)
    # commit to databse
    db.session.commit()

    msg = Message(
        f"Welcome to Shoha's Bike Shop!",
        body='Thank you for joining our mailing list. We sell only the biest bikes. Stay tuned for more deals and fire cops.',
        recipients=[email]
    )

    mail.send(msg)

    return {
        'status': 'ok',
        'message': f"Successfully created an account for {username}.",
        'user': user.to_dict()
    }


@auth.route('/api/login', methods=["POST"])
def apiLogMeIn():
    data = request.json

    username = data['username']
    password = data['password']

    # check if user exists
    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': f"Welcome back, {username}",
                'user': user.to_dict()
            }
        else:
            return {
                'status': 'not ok',
                'message': "Invalid password."
            }
    else:
        return {
            'status': "not ok",
            'message': "A user with that username does not exist."
        }
