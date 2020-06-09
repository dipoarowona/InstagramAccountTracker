import pymongo, config, time
from datetime import datetime
from accountProcessing import instaAccount

client = pymongo.MongoClient(config.mongo_uri)
db = client[config.mongo_db]
col = db[config.mongo_collection]

def followersData(email):
    data = list(col.find({"email":email},{"_id":0, "followers":1}))
    values = []
    dates = []
    for i in range(len(data[0]["followers"])): 
        value = list(data[0]["followers"][i].values())[0]
        date = list(data[0]["followers"][i].keys())[0]
        values.append(value)
        dates.append(date)
    return dates,values

def likesData(email):
    
    data = list(col.find({"email":email},{"_id":0, "likes":1}))
    values = []
    dates = []
    for i in range(len(data[0]["likes"])): 
        value = list(data[0]["likes"][i].values())[0]
        date = list(data[0]["likes"][i].keys())[0]
        values.append(value)
        dates.append(date)
    if values[0]==None:
        return dates,None
    return dates,values
 
    

def postsData(email):
    
    data = list(col.find({"email":email},{"_id":0, "numOfPic":1}))
    values = []
    dates = []
    for i in range(len(data[0]["numOfPic"])): 
        value = list(data[0]["numOfPic"][i].values())[0]
        date = list(data[0]["numOfPic"][i].keys())[0]
        values.append(value)
        dates.append(date)
    return dates,values
    
def avgLikesData(email):
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
        pass

print(followersData("abdulsalam.arowona@gmail.com")[0])
print('\n\n\n\n\n', likesData("abdulsalam.arowona@gmail.com"))
print("\n\n\n\n\n", postsData('abdulsalam.arowona@gmail.com'))
print("\n\n\n\n\n", avgLikesData('abdulsalam.arowona@gmail.com'))