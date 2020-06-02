
#pull all ig accounts from database - done
#create instance of account processing class once a day for all accounts
#add the updated info to the database
import pymongo, config, time
from datetime import datetime
from accountProcessing import instaAccount

client = pymongo.MongoClient(config.mongo_uri)
db = client[config.mongo_db]
col = db[config.mongo_collection]

while True:
    accounts = list(col.find({},{"igAccount":1,"_id":1}))#retrieve data
    print(accounts)
    for account in accounts:
        user = instaAccount(account["igAccount"])
        
        if user.isPublic and user.isAccount:

            temp = user.followingFollowersPosts()
            likes = user.likes()
            followers = int(temp[0]) 
            following = int(temp[1])
            posts = int(temp[2])
            date = datetime.now().strftime("%m/%d/%Y")
            col.update_one( {"_id":account["_id"]} , { "$push": { "followers":{date :followers} } } )
            col.update_one( {"_id":account["_id"]} , { "$push": { "following":{date :following} } } )
            col.update_one( {"_id":account["_id"]} , { "$push": { "likes":{date :likes} } } )
            col.update_one( {"_id":account["_id"]} , { "$push": { "numOfPic":{date :posts} } } )

            print("ACCOUNT: ", account["igAccount"])
            print("ID: ", account["_id"] )
            print("CURRENT TIME", datetime.now())
            print("FOLLOWERS : ", following)
            print("FOLLOWING: ", followers)
            print("LIKES: ", likes)
            print("NUMBER OF POSTS: ", posts)
            print("DATABASE UPDATED.\n")
        else:
            print("account does not exist or is private")
    print("\n\n\n\n")
    time.sleep(660)


print("info updated")


#USED TO RESET DATABASE ONCE TESTING IS DONE

# col.insert_one({
#     "name": "Nnenna",
#     "email" : "nnenna@test.com",
#     "password": "password2",
#     "igAccount": "_nnennaya",
#     "followers": [{
#         datetime.now().strftime("%m/%d/%Y"): 1234
#     }],
#     "following": [{
#         datetime.now().strftime("%m/%d/%Y"): 1234
#     }],
#     "likes":[{
#         datetime.now().strftime("%m/%d/%Y"): 1234
#     }],
#     "numOfPic":[{
#         datetime.now().strftime("%m/%d/%Y"): 1234
#     }]
# })