from flask import Flask, render_template, abort, session, redirect, url_for
from forms import SignUpForm, LoginForm, EditPetForm
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)

# Model for Pets
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    postedBy =  db.Column(db.String, db.ForeignKey('user.id'))

# Model for Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    pets = db.relationship('Pet', backref = 'user')

# Creates the tables
db.create_all()

# Create "team" user and add it to session
team = User(name = "Pet Rescue Team", email = "team@petrescue.co", password = "adminpass")
db.session.add(team)

# Create all pets
nelly = Pet(name = "Nelly", age = "5 weeks", bio = "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name = "Yuki", age = "8 months", bio = "I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name = "Basker", age = "1 year", bio = "I love barking. But, I love my friends more.")
mrfurrkins = Pet(name = "Mr. Furrkins", age = "5 years", bio = "Probably napping.")

# Add all pets to the session
db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)

# Commit changes in the session
try:
    db.session.commit()
except Exception as e: 
    db.session.rollback()
finally:
    db.session.close()

@app.route("/")
def homepage():
    """View function for Home Page."""
    pets = Pet.query.all()
    return render_template("home.html", pets = pets)

@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>", methods=['GET', 'POST'])
def pet_details(pet_id):
    """View function for Showing Details of Each Pet.""" 
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    elif form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data

        # Commit changes in the session
        try:
            db.session.commit()
        except Exception as e: 
            db.session.rollback()
            return render_template("details.html", pet = pet, form = form, message = 'A pet with that name already exist!')

    return render_template("details.html", pet = pet, form = form)

@app.route('/delete/<int:pet_id>')
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet:
        db.session.delete(pet)
        try:
            db.session.commit()
        except Exception as e: 
            db.session.rollback()
        finally:
            db.session.close()
            return redirect(url_for('homepage'))
    else:
        abort(404, description="No Pet was Found with the given ID")
    

@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    # Add a new user if the validation check passes
    if form.validate_on_submit():
        # Create a new user with the form parameters
        newUser = User(name = form.name.data, email = form.email.data, password = form.password.data)
        # Add the user to the database session
        db.session.add(newUser)
        # Try to commit the changes to the database session
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            # If we are caught in in the exception, it means that the uniqe flag for email was raised,
            # therfore, we render the template agin with a message to the user that the email already
            # exist
            return render_template("signup.html", form = form, message = "This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()
        # Render the template again with a successs message
        return render_template("signup.html", message = "Success!")
    # Default view for the sign up page
    return render_template("signup.html", form = form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    # Authenticate user
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data, User.password == form.password.data).first()
        if user:
            print("I am a print statment in login")
            session['user'] = user.id
            return render_template("login.html", message = "Login Succesfull!")
        else:
            return render_template("login.html", message = "Invalid Credentials", form = form)
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('homepage'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
