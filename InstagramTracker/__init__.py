from flask import Flask


#import config page later



app = Flask(__name__)
app.config["SECRET_KEY"] = 'e3da129cac7f4aff0535190937f75aed36dcdeb9ac4777c6ac9a5d89b9574bfe'


from InstagramTracker import routes
