from main import db
from datetime import datetime

class User(db.Model):
    """Contains all the information for a User. Instantiation requires
    name, username, email, password, location and motto.

    Flask-sqlalchemy takes care of all the heavy lifting for database
    interation."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(40))
    location = db.Column(db.String(80))
    motto = db.Column(db.String(120))
    sign_up_day = db.Column(db.String(40))
    
    def __init__(self, name, username, email, password, location, motto):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.location = location
        self.motto = motto
        self.sign_up_day = datetime.utcnow()
        
    def __repr__(self):
        return '<User %r>' % self.username
        
class Beer(db.Model):
    """Beer object, takes care of everything you would want to know 
    about a specific beer."""
    
    # Attributes specific to this particular beer
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    abv = db.Column(db.Float)
    photo = db.Column(db.String(200))
    special_ingredient = db.Column(db.String(250))
    
    # Relationships to other models
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    genre = db.relationship('Genre', backref = db.backref('beers', lazy='dynamic'))
    brewery_id = db.Column(db.Integer, db.ForeignKey('brewery.id'))
    brewery = db.relationship('Brewery', backref = db.backref('beers', lazy='dynamic'))
    
    def __init__(self, name, abv, photo, special_ingredient, genre, brewery):
        self.name = name
        self.abv = abv
        self.photo = photo
        self.special_ingredient = special_ingredient
        self.genre = genre
        self.brewery = brewery
        
    def __repr__(self):
        return '<Beer %r>' % self.name
        
class Brewery(db.Model):
    """Brewery object."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(120))
    
    def __init__(self, name, location):
        self.name = name
        self.location = location
        
    def __repr__(self):
        return '<Brewery %r>' % self.name
        
class Rating(db.Model):
    """Rating object for a beer, from a user."""
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    scale = db.Column(db.Integer)
    notes = db.Column(db.Text)
    session_beer = db.Column(db.Integer)
                  
    # Relationships to other models
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', 
                           backref = db.backref('user', lazy='dynamic'))
        
    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'))
    beer = db.relationship('Beer',
                           backref = db.backref('beer', lazy='dynamic'))

    def __init__(self, score, scale, notes, session_beer, user, beer):
        self.score = score
        self.scale = scale
        self.notes = notes
        self.session_beer = session.beer
        self.user = user
        self.beer = beer
        
    def __repr__(self):
        return '<Rating %r>' % (self.score + '/' + self.scale)
    
class Genre(db.Model):
    """Genre of the beer."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    typical_attributes = db.Column(db.Text)
    
    def __init__(self, name, typical_attributes):
        self.name = name
        self.typical_attributes = typical_attributes
        
    def __repr__(self):
        return '<Genre %r>' % self.name

class Blog(db.Model):
    """Blog feature for use in creating main pages for the site."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    slug = db.Column(db.String(80), unique=True)
    created_on = db.Column(db.String(40))
    text = db.Column(db.Text)

    # Relationship specifics
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref = db.backref('posts', lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref = db.backref('author', lazy='dynamic'))

    def __init__(self, title, category, text, author):
        self.title = title
        self.slug = slugify(title)
        self.category = category
        self.created_on = datetime.utcnow()
        self.text = text
        self.author = author

    def __repr__(self):
        return '<Post %r>' % (self.slug + ', ' + self.category)

class Category(db.Model):
    """Category object for grouping posts to sections of the site."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __init__(self, name):
        self.name = slugify(name)

    def __repr__(self):
        return '<Category %r>' % self.name

def slugify(string_text):
    slug = ''
    for char in string_text:
        if char == ' ':
            slug += '-'
        else:
            slug += char
    return slug
