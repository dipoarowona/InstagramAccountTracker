from InstagramTracker import app, login_manager, db, bcrypt
from flask import render_template, flash, redirect, url_for, request
from InstagramTracker.forms import LoginForm, RegisterForm
from flask_login import login_user, current_user,login_required, logout_user, LoginManager, UserMixin
from datetime import datetime
import datetime as dt
import flask, json
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

    if current_user.is_authenticated:
        return redirect(url_for('main'))

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

    header = headerData()
    like=header[2]

    er = engagement()
    ffratio = ratio()
    income=money(er)
    if current_user.likes ==[]:
        like=None
    
    return render_template("main.html", following=header[0], followers=header[1],
                            likes=like, posts=header[3], changeFollowing=header[5],
                            changeFollowers=header[4], changeLikes=header[6], changePosts=header[7], 
                            engagement=er, ratio=ffratio[0],ratiodesc=ffratio[1], money=income)

@app.route('/logout', methods = ['GET'])    
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/data', methods=["GET","POST"])
@login_required
def data():
    flwrsData = followersData(current_user.email)
    lksData = likesData(current_user.email)
    avgLikesData = averageLikesData(current_user.email)

    try:
        response = app.response_class( 
            response=json.dumps([{'followerData':flwrsData[1], 'followersLabels':flwrsData[0]},
                                {'likesData':lksData[1], 'likesLabels':lksData[0]},
                                {'avgLikesData':avgLikesData[1], 'avgLikesLabels':avgLikesData[0]}
                                ]),
            status=250,
            mimetype='application/json'
        )
    except:
        response = app.response_class( 
            response=json.dumps([{'followerData':None, 'followersLabels':None},
                                {'likesData':None, 'likesLabels':None},
                                {'avgLikesData':None, 'avgLikesLabels':None}
                                ]),
            status=250,
            mimetype='application/json'
        )


    
    return response


def headerData():
    try:
        followers = followersData(current_user.email)[1][-1]
    except:
        followers = 0
   
    try:
        data = list(current_user.following)
        lst = []
        for i in data:
            lst.append(list(i.values())[0])
        following = lst[-1]
    except:
        following = 0
    
    try:
        likes = likesData(current_user.email)[1][-1]
    except:
        likes = None
    
    try:
        posts = postsData(current_user.email)[1][-1]
    except:
        posts = 0
    
    try:
        changeFollowing = (following-lst[-2])/following
    except:
        changeFollowing = 0.0 
    
    try:
        changeFollowers = (followers-followersData(current_user.email)[1][-2])/followers
    except:
        changeFollowers = 0.0

    try: 
        changeLikes = (likes-likesData(current_user.email)[1][-2])/likes
    except:
        changeLikes = 0.0 
    try:
        changePosts =(posts-postsData(current_user.email)[1][-2])/posts
    except:
        changePosts = 0.0
    
    changePosts = round(changePosts,4)
    changeFollowers = round(changeFollowers,4)
    changeFollowing = round(changeFollowing,4)
    changeLikes = round(changeLikes,4)

    return following, followers, likes, posts, changeFollowers, changeFollowing, changeLikes, changePosts
def followersData(email):
    data = list(current_user.followers)
    values = []
    dates = []
    for i in range(len(data)): 
        value = list(data[i].values())[0]
        date = list(data[i].keys())[0]
        values.append(value)
        dates.append(date)
    return dates,values
def likesData(email):
    try:
        data = list(current_user.likes)
        values = []
        dates = []
        for i in range(len(data)): 
            value = list(data[i].values())[0]
            date = list(data[i].keys())[0]
            values.append(value)
            dates.append(date)
        if values[0]==None:
            return dates,None
        return dates,values
    except:
        pass
def engagement():
    try:
        avglikes = averageLikesData(current_user.email)[1][-1]
        followers = list(current_user.followers)[-1][datetime.now().strftime("%m/%d/%Y")]
        return round(avglikes/followers*100,2)
    except:
        return 0
def postsData(email):
    data = list(current_user.numOfPic)
    values = []
    dates = []
    for i in range(len(data)): 
        value = list(data[i].values())[0]
        date = list(data[i].keys())[0]
        values.append(value)
        dates.append(date)
    return dates,values   
def averageLikesData(email):
    try:
        likes = likesData(email)
        posts = postsData(email)
        avg=[]
        
        for i in range(len(likes[0])):
            if likes[0][i] == posts[0][i]:
                temp = round(likes[1][i]/posts[1][i],3)
                avg.append(temp)
        return likes[0], avg
    except:
        return[None,None]
def ratio():
    try:
        followers = followersData(current_user.email)[1][-1]
        following = current_user.following[-1][datetime.now().strftime("%m/%d/%Y")]
        ratio = followers/following
        desc = ''
        if ratio <= 0.5:
            desc = 'Spammer'
        elif ratio >0.5 and ratio <=1:
            desc = 'Suspicious'
        elif ratio >1 and ratio <=2:
            desc = 'Normal'
        elif ratio >2 and ratio <=10:
            desc = 'Micro Influencer'
        elif ratio >10:
            desc = 'Influencer'
        return [round(ratio,2), desc]
    except:
        return [0, 'Undetermined']


def money(ratio):
    try:
        return round((ratio/100)*(current_user.followers[-1][datetime.now().strftime("%m/%d/%Y")])*(ratio/100), 2)
    except:
        return 0
