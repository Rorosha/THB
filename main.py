import os

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

import models

app = Flask(__name__)
SQL_DATABASE = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + SQL_DATABASE + '/beers.db'
db = SQLAlchemy(app)
#SECRET_KEY = os.urandom(24)
SECRET_KEY = '987NNJI:LKJ876A:LKSJD:SLKAJS654DKJG23H'
app.config.from_object(__name__)

@app.route('/')
def show_home():
    if session['logged_in'] == False:
        beers = models.Beer.query.first_or_404()
        username = 'Login'
        return render_template('index.html', beers=beers, username=username)
    else:
        beers = models.Beer.query.first_or_404()
        username = session['username']
        return render_template('index.html', beers=beers, username=username)

@app.route('/home')
def user_landing():
    if session['logged_in'] == True:
        beers = models.Beer.query.first()
        username = session['username']
        return render_template('user_landing.html', beers=beers, 
                               username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            user = models.User.query.filter_by(username=request.form['username']).first()
            if pw_hash(request.form['password']) == user.password:
                session['logged_in'] = True
                session['username'] = user.name
                flash('You were logged in')
                return redirect(url_for('user_landing'))
            else:
                session['logged_in'] = False
                error = 'Invalid username/password. Have you registered?'

        except:
               error = 'Invalid username/password. Have you registered?'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = 'Login'
    return redirect(url_for('show_home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':

        for arg in request.form:
            if request.form[arg] == '':
                error = 'Field %r was empty' % arg
                return render_template('register.html', error=error)
            else:
                pass

        try:
            if request.form['password'] == request.form['password_check']: 
                if email_check(request.form['email']):
                    new_user = models.User(request.form['name'],
                                           request.form['username'],
                                           request.form['email'],
                                           pw_hash(request.form['password']),
                                           request.form['location'],
                                           request.form['motto'])
                    db.session.add(new_user)
                    db.session.commit()
                    
                else: 
                    error = "Please enter a correctly formatted email address."
                    return render_template('register.html', error=error)

            else:
                error = "Your passwords didn't match. Try again."
                return render_template('register.html', error=error)

            return redirect(url_for('login'))
        except:
            error = 'One of your fields was filled out in correctly. Please try again.'

    return render_template('register.html', error=error)

@app.route('/addbeer', methods=['GET', 'POST'])
def add_beer():
    error = None

    if session['logged_in'] == True:

        if request.method == 'POST':
            
            genre = models.Genre.query.filter_by(
                name=request.form['genre']).first()
            brewery = models.Brewery.query.filter_by(
                name=request.form['brewery']).first()

            if genre is None or brewery is None:
                error = "List a valid Genre or Brewery..."
                return render_template('add_beer.html', error=error)

            new_beer = models.Beer(
                request.form['name'],
                request.form['abv'],
                request.form['photo'],
                request.form['special'],
                genre,
                brewery)

            # For some reason this needs to be a merge() instead of an
            # add(), but I have no idea why. There be dragons...Or,
            # I'm a retard.
            db.session.merge(new_beer)
            db.session.commit()

            # Set the session to remember the beer just added
            session['newest_beer'] = request.form['name']

            return redirect(url_for('beer_landing'))

        else: # ends POST
            
            return render_template('add_beer.html')
            
    else: # ends logged in
        return redirect(url_for('show_home'))

@app.route('/beer_landing')
def beer_landing():
    error = None
    beers = models.Beer.query.first_or_404()
    added_beer = models.Beer.query.filter_by(name=
                                             session['newest_beer']).first()

    return render_template('beer_landing.html', added_beer=added_beer, beers=beers)

# Utility functions - will be moved to another module later

def email_check(email):
    """Checks to make sure user inputted email actually conforms to what an
    email should look like. Returns True if everthing looks right."""
    try:
        pieces = email.split('@')
        if ' ' not in pieces[0] and '.' in pieces[1]:
            return True
    except:
        return False

def pw_hash(pw):
    """Takes a string, and creates a hexdigest. Keeps us from needing to store
    actual passwords..."""
    import hashlib
    pw_digest = hashlib.new('sha1')
    pw_digest.update(str(pw))
    return pw_digest.hexdigest()

if __name__ == '__main__':
    app.debug = True
    app.run()
