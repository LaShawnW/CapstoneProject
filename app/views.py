from app import app, db, login_manager
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
import datetime
from app.models import Users
from app.forms import LoginForm, UserRegistration, ReservationForm
import stripe
import time
from flask_socketio import SocketIO,emit,join_room

public_key = 'pk_test_l5lotlN2Ys6OhMMYi6p7Wq7m00yAMKQtNO'
stripe.api_key = "	sk_test_W5gBcbCxQipyN94e9pPWm3Bu00Tfhvtrwk"
socketio=SocketIO(app )


###
# Routing for your application.
###
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/myaccount')
@login_required
def account():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('myaccount.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        
        return redirect(url_for('account'))


    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.email.data:
            email = form.email.data
            password = form.password.data 

            user = Users.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True


            login_user(user, remember=remember_me)
            next_page = request.args.get('next')

            print (next_page)

            flash('Logged in successfully.', 'success')
            return redirect(next_page or url_for("account"))
        else:
            flash('Username or Password is incorrect.', 'danger')


    flash_errors(form)
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))



@app.route('/register', methods=['GET','POST'])
def register():
    """accepts user information and save it to the database"""  
    form=UserRegistration()
    # now = datetime.datetime.now()
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            gender = form.gender.data 
            email = form.email.data
            password = form.password.data

            user = Users(firstname,lastname,gender,email,password)

            db.session.add(user)
            db.session.commit()

            flash('User information submitted successfully.', 'success')
        else:
            flash('User information not submitted', 'danger')
        
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/reserve', methods=['GET','POST'])
def reserve():
    """accepts user information and save it to the database"""  
    form=ReservationForm()
    # now = datetime.datetime.now()
    if request.method == 'POST':
        if form.validate_on_submit():
            starttime = form.starttime.data
            startdate = form.startdate.data
            endtime = form.endtime.data 
            enddate = form.enddate.data
            parkinglots = form.parkinglots.data
            typeofparking = form.typeofparking.data
            licenseplateno = form.licenseplateno.data

            reservation = Reservations(starttime,startdate,endtime,enddate,parkinglots,typeofparking, licenseplateno)

            db.session.add(reservation)
            db.session.commit()

            flash ('Congrats! You have successfully made your reservation.', 'success')
        else:
            flash('Oh no! Looks like this parking lot is full. Please try another.', 'danger')
        
        return redirect(url_for("account"))
    return render_template("reserve.html", form=form)

'''def checkspaces():
    parking = ParkingLots.query.all()

    if '''


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/chat2')
# @login_required
def chat2():
    date = format_date_joined()
    return render_template('chat2.html',date=date)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error), 'danger')


def format_date_joined():
    datetime.datetime.now()
    date_joined = datetime.datetime.now()
    return "Today is "     + date_joined.strftime("%A,%B,%d ,%Y") 


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route('/thanks')
@login_required
def thankyou():
    return render_template('thanks.html')

@app.route('/payment', methods=['POST'])
def payment():
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    stripe.Charge.create(
            customer=customer.id,
            amount=1999,
            currency='usd',
            description='Donation'
    )
        
    return redirect(url_for('thankyou'))
    

@app.route('/purchase')
@login_required
def purchase():
    date = format_date_joined()
    return render_template('purchase.html', date=date,public_key=public_key)

if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True, host="0.0.0.0", port="8080")
