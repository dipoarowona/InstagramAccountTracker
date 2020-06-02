from InstagramTracker import app, login_manager, db, bcrypt
from flask import render_template, flash, redirect, url_for, request
from InstagramTracker.forms import LoginForm, RegisterForm
from flask_login import login_user, current_user,login_required, logout_user, LoginManager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
    
class User(UserMixin, db.Document):
    meta = {'collection': 'Users'}
    name =  db.StringField()
    email = db.StringField(max_length=30)
    igAccount = db.StringField()
    password = db.StringField()
    followers = db.ListField(db.MapField(field=db.StringField()))
    following = db.ListField(db.MapField(field=db.StringField()))
    likes = db.ListField(db.MapField(field=db.StringField()))
    numOfPic = db.ListField(db.MapField(field=db.StringField()))


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated == True:
        return redirect(url_for('main'))
    if form.validate_on_submit():
        check_user = User.objects(email=form.email.data).first()
        if check_user and bcrypt.check_password_hash(check_user.password,form.password.data):
            login_user(check_user)
            return redirect(url_for("main"))
        else:
            flash("Invalid Email or Password.","danger")
    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=["GET",'POST'])
def register():
    form =  RegisterForm()

    if form.validate_on_submit() and request.method == 'POST':
        existing_users = User.objects(email=form.email.data).first()
        if existing_users is None:
            hashedpw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            hey = User(name = form.name.data, email = form.email.data, igAccount=form.igAccount.data, password=hashedpw, followers=[], following=[],likes=[],numOfPic=[]).save()
            flash("Account Has Been Created!", 'success')
            return  redirect(url_for('login'))
        else:
            flash("Account With That Email Is Already In Use.", 'danger')
    return render_template('register.html', title="Sign Up", form=form)

@app.route("/accountsummary")
@login_required
def main():
    return render_template("main.html")

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))