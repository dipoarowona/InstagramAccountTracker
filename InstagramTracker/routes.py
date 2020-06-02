from InstagramTracker import app, login_manager, db, bcrypt
from flask import render_template, flash, redirect, url_for, request
from InstagramTracker.forms import LoginForm, RegisterForm
from flask_login import login_user, current_user,login_required, logout_user, LoginManager
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime



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
            login_user(check_user,remember=form.remember.data)
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
    following = 0 if not current_user.following else current_user.following[-1][datetime.now().strftime("%m/%d/%Y")]
    followers = 0 if not  current_user.followers else current_user.followers[-1][datetime.now().strftime("%m/%d/%Y")]
    likes = 0 if not current_user.likes else current_user.likes[-1][datetime.now().strftime("%m/%d/%Y")]
    posts = 0 if not current_user.numOfPic else current_user.numOfPic[-1][datetime.now().strftime("%m/%d/%Y")]
# yestereday date time needed
    changeFollowing = 0.0 if following is None or not following or current_user.following[-2][datetime.now().strftime("%m/%d/%Y")] is None else (following-current_user.following[-2][datetime.now().strftime("%m/%d/%Y")])/following
    changeFollowers = 0.0 if followers is None or not followers or  current_user.followers[-2][datetime.now().strftime("%m/%d/%Y")] is None else (followers-current_user.followers[-2][datetime.now().strftime("%m/%d/%Y")])/followers
    changeLikes = 0.0 if likes is None or not likes or current_user.likes[-2][datetime.now().strftime("%m/%d/%Y")] is None else (likes-current_user.likes[-2][datetime.now().strftime("%m/%d/%Y")])/likes
    changePosts = 0.0 if posts is None or not posts or current_user.numOfPic[-2][datetime.now().strftime("%m/%d/%Y")] is None else (posts-current_user.numOfPic[-2][datetime.now().strftime("%m/%d/%Y")])/posts
    print(changePosts,changeFollowers, changeFollowing, changeLikes)
    return render_template("main.html", following=following, followers=followers,
                            likes=likes, posts=posts, changeFollowing=changeFollowing,
                            changeFollowers=changeFollowers, changeLikes=changeLikes, changePosts=changePosts)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))