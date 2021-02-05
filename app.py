from flask import Flask, render_template, abort, session, redirect, url_for
from forms import SignUpForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

"""Information regarding the Pets in the System."""
pets = [
            {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
            {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
            {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
            {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."}, 
        ]

"""Information regarding the Users in the System."""
users = [
            {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"},
        ]

@app.route("/")
def homepage():
    """View function for Home Page."""
    return render_template("home.html", pets = pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    """View function for Showing Details of Each Pet.""" 
    pet = next((pet for pet in pets if pet["id"] == pet_id), None) 
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet = pet)

@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    # Add a new user if the validation check passes
    if form.validate_on_submit():
        newUser = {"id": len(users) + 1, "full_name": form.name.data,
            "email": form.email.data, "password": form.password.data}
        users.append(newUser)
        return render_template("signup.html", message = "Success!")

    return render_template("signup.html", form = form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    # Authenticate user
    if form.validate_on_submit():
        for user in users:
            if user["email"] == form.email.data and user["password"] == form.password.data:
                session["user"] = user
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
