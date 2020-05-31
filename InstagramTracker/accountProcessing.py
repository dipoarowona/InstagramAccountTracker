import requests
import re
import selenium
from selenium import webdriver 
import time
from datetime import datetime

class instaAccount:
    r = ''
    username = ''
    url = ''
    def __init__(self, username):
        self.url = 'https://www.instagram.com/' + username
        self.r = requests.get(self.url).text
        self.username = username
            
    def isAccount(self):
        start = '"edge_followed_by":{"count":'
        end = '},"followed_by_viewer"'
        validate = self.r[self.r.find(start)+len(start):self.r.rfind(end)]
        if len(validate) > 1000:
            return False
        else:
            return True

    def isPublic(self):
        if self.isAccount():
            start = 'is_private":'
            end = ',"is_verified":'
            private = self.r[self.r.find(start)+len(start):self.r.rfind(end)]
            if private == "false":
                return True
            return False
    
    def followingFollowersPosts(self):
        if self.isAccount():
            start = '"edge_followed_by":{"count":'
            end = '},"followed_by_viewer"'
            followers= self.r[self.r.find(start)+len(start):self.r.rfind(end)]

            start = '"edge_follow":{"count":'
            end = '},"follows_viewer"'
            following= self.r[self.r.find(start)+len(start):self.r.rfind(end)]

            start = 'edge_owner_to_timeline_media":{"count":'
            end = ',"page_info":{"has_next_page":'
            post = self.r[self.r.find(start)+len(start):[postEnd.start() for postEnd in re.finditer(end, self.r)][1]]

            return(followers, following, post)

    def likes(self):
        if self.isAccount() and self.isPublic():
            s = datetime.now()
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            driver = webdriver.Chrome("/Users/dipoarowona/Downloads/chromedriver", options=options)
            driver.get(self.url)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            posts = []
            while(match==False):
                lastCount = lenOfPage
                time.sleep(3)
                links = driver.find_elements_by_tag_name('a')
                for link in links:
                    post = link.get_attribute('href')
                    if '/p/' in post:
                        posts.append( post )
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
                
            posts = set(posts)#get rid of duplicates of post links

            #get likes for each post "edge_media_preview_like":{"count":
            likes = 0
            counter = 0
            for post in posts:

                posturl = post
                postr = requests.get(posturl).text

                start = '"edge_media_preview_like":{"count":'
                end = ',"edges":[]},'

                postlike = postr[postr.find(start)+len(start):postr.rfind(end)]
                likes = likes +  int(postlike)
                counter+=1

            e = datetime.now()

            return(likes)


while True:
    time.sleep(1800)
    user = instaAccount("latifaarowona")
    if user.isPublic and user.isAccount:
        print(datetime.now())
        print(user.followingFollowersPosts())
        print(user.likes(),"\n\n\n\n")
    else:
        print("account does not exist or is private")
