from InstagramTracker import app
from flask import render_template, flash, redirect, url_for
from InstagramTracker.forms import LoginForm, RegisterForm
from flask_login import login_user, current_user,login_required, logout_user, LoginManager


@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = {"email":"test@arowona.com","password":"test"}
        if form.email.data == 'test@arowona.com' and form.password.data == 'test':

            return redirect(url_for("main"))
    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=["GET",'POST'])
def register():
    form =  RegisterForm()
    if form.validate_on_submit():
        flash("Account Has Been Created!", 'success')
        return  redirect(url_for('login'))
    return render_template('register.html', title="Sign Up", form=form)

@app.route("/accountsummary")
def main():
    return render_template("main.html")