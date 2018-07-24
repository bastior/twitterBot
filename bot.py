from twitter import Twitter, OAuth, TwitterHTTPError
import os
import sys
import time
import random
import datetime



class Bot:
    def __init__(self):
        self.connection = 0
        self.name = "Iamnotabot4";
        self.logFile = open("log.txt",'a')
        self.logFile.write("\n###########################################################\n")
        self.logFile.write("## "+self.getDateTime()+"New Sesion has been created ##\n")
        self.logFile.write("###########################################################\n")
        random.seed()

    def connect(self):
        try:
            self.connection = Twitter(auth=OAuth("PURGED CREDENTIALS WILL NOT WORK NOW."))
            self.logFile.write(self.getDateTime() + "\tConncetion succeeded")
        except Exception,e:
            self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))

    def delay (self):
        min_time = 5
        max_time = 20
        toWait = random.randint(min_time, max_time)
        if toWait > 0:
            time.sleep(toWait)

    def getDateTime(self):
        return str(datetime.datetime.now())

    def tweet(self,text):
        try:
            self.connection.statuses.update(status=text)
            self.logFile.write('\n'+self.getDateTime()+"\tTweet has been send with text: " + text)
        except Exception,e:
            self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))

    def getFollowers(self, userId = ""):
        try:
            if userId == "":
                userId = self.name
            followers_status = self.connection.followers.ids(screen_name = userId)
            followers = set(followers_status["ids"])

            string = ""
            for follower in followers:
                string+=str(follower)
                string+=","
            string = string[:-1]
            lookedUp = self.connection.users.lookup(user_id=string)

            with open("followersLookedUp.txt", "w") as out_file:
                for follower in lookedUp:
                    out_file.write("%s\n" % (follower["screen_name"]))
            self.logFile.write('\n'+self.getDateTime()+"\tFollowers table has been filled in 'followersLookedUp.txt'")

            with open("followers.txt", "w") as out_file:
                for follower in followers:
                    out_file.write("%s\n" % (follower))
            self.logFile.write('\n'+self.getDateTime()+"\tFollowers table by ID has been filled in 'followers.txt'")
        except Exception,e:
            self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))

    def getFollowed(self, userId = ""):
        if userId == "":
            userId = self.name
        followers_status = self.connection.friends.ids(screen_name = userId)
        followers = set(followers_status["ids"])

        string = ""
        for follower in followers:
            string+=str(follower)
            string+=","
        string = string[:-1]

        lookedUp = self.connection.users.lookup(user_id=string)

        with open("followedLookedUp.txt", "w") as out_file:
            for follower in lookedUp:
                #print follower
                out_file.write("%s\n" % (follower["screen_name"]))
        self.logFile.write('\n'+self.getDateTime()+"\tFollowed table has been filled in 'followedLookedUp.txt'")

        with open("followed.txt", "w") as out_file:
            for follower in followers:
                out_file.write("%s\n" % (follower))
        self.logFile.write('\n'+self.getDateTime()+"\tFollowed table by ID has been filled in 'followed.txt'")

    def getTweetsByPhrase(self,phrase,count,result_type):
        self.logFile.write('\n'+self.getDateTime()+"\tSearching "+str(count)+' '+result_type+" tweets by phrase -  "+phrase+ "...")
        result = self.connection.search.tweets(q=phrase, result_type=result_type, count=count)
        with open("foundTweets.txt","a") as out_file:
            out_file.write("----- Phrase: %s -----\n" % (phrase))
            for i in range(0,count):
                try:
                    author = result["statuses"][i]["user"]["screen_name"]
                    text = result["statuses"][i]["text"]
                    tweet = "Autor: "+author+"\tTekst: "+text.encode('ascii','ignore')
                    out_file.write("%s\n" % tweet)
                except Exception,e:
                    self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))
            out_file.write("----------------------------------------------\n")
        self.logFile.write('\n'+self.getDateTime()+"\t'foundTweets.txt' has been updated")
        return result

# DO NOT OVERUSE IT. IT IS WORKING
# DO NOT PUT HIGH VALUE IN COUNT 
# followed.txt and followers.txt Must be valid and up to date
#
# Function will autofollow first (count) number of people that follows you but you do not follow yet

    def returnFollowed (self):
        followedList = []
        with open("followed.txt", "r") as in_file:
            for line in in_file:
                followedList.append(int(line))

        return set(followedList)

    def returnFollowers (self):
        followedList = []
        with open("followers.txt", "r") as in_file:
            for line in in_file:
                followedList.append(int(line))

        return set(followedList)

    def autoRefollow (self, count = 1):
        self.logFile.write('\n'+self.getDateTime()+"\tRefollow "+str(count)+" users that follow you")
        diff = self.returnFollowers() - self.returnFollowed()
        diff = list(diff)[:count]

        for user in diff:
            try:
                self.connection.friendships.create(user_id=user, follow=False)
                self.delay()
                self.logFile.write('\n'+self.getDateTime()+"\tUser with ID: "+str(user)+" is now followed")
            except Exception,e:
                self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))
                return

# SAME AS autoRefollow fnc, do not overuse

    def autoFollowFollowersOfUser (self, user, count = 2):
        self.logFile.write('\n'+self.getDateTime()+"\t'Follow "+str(count)+ " random users that follow "+user)
        followedList = self.returnFollowed()
        followersOfUser = set(self.connection.followers.ids(screen_name=user)["ids"][:count])

        followersOfUser = followersOfUser - followedList

        for user_id in followersOfUser:
            try:
                self.delay()
                self.connection.friendships.create(user_id=user_id, follow=False)
                self.logFile.write('\n'+self.getDateTime()+"\tUser with ID: "+str(user_id)+" is now followed")
            except Exception,e:
                self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))
                return

    def unfollowUsersNonFollowU(self,count = 2):
        self.logFile.write('\n'+self.getDateTime()+"\tUnfollow "+str(count)+" users that not followed u back")
        followedUsers = set(self.connection.friends.ids(screen_name = "")["ids"][:count])
        followersList = self.returnFollowers()
        followedUsers = followedUsers-followersList
        for user_id in followedUsers:
            try:
                self.delay()
                self.connection.friendships.destroy(user_id = user_id)
                self.logFile.write('\n'+self.getDateTime()+"\tUser with ID: "+str(user_id)+" is no more followed")
            except Exception,e:
                self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))
                return

    def getTrendsByLocation(self,LocationId):
        self.logFile.write('\n'+self.getDateTime()+"\tSearching trends by location ID -  "+str(LocationId)+ "...")
        results = self.connection.trends.place(_id = LocationId)
        location = results[0]["locations"][0]["name"]
        with open("trends.txt", "a") as out_file:
            out_file.write("%s Location: %s\n" % (str(datetime.datetime.now()),location))
            for trend in results[0]["trends"]:
                print " - %s" % trend["name"].encode('ascii','ignore')
                out_file.write("%s\t" % trend["name"].encode('ascii','ignore'))
        self.logFile.write('\n'+self.getDateTime()+"\t'trends.txt' has been updated")

    def retweetByPhrase(self, phrase, count = 2, result_type="recent"):
        self.logFile.write('\n'+self.getDateTime()+"\tRetweet "+str(count)+' '+result_type+" tweets by phrase - "+phrase+" ...")
        result = self.getTweetsByPhrase(phrase, count, result_type)

        for tweet in result["statuses"]:
            try:
                self.delay()
                self.connection.statuses.retweet(id=tweet["id"])
                self.logFile.write('\n'+self.getDateTime()+"\tTweet with text: '"+tweet["text"]+"' has been retweeted")
            except Exception,e:
                self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))

#    def MostFollowFromFollowed(self,count = 2):
#        AllFollowedUsers = self.returnFollowed()
#        for followedUser in AllFollowedUsers:
#            print followedUser
#            print "-----"
#            followedOfUser = set(self.connection.friends.ids(user_id = followedUser)["ids"][:count])
#            for user in followedOfUser:
#                print "count:"
#                self.delay();
#                print self.connection.users.lookup(user_id=followedOfUser)

    def retweetMostPopular (self, toFind = 10):
        self.logFile.write('\n'+self.getDateTime()+"\t'Searching "+str(toFind)+" most recent tweets on wall ...")
        tweetsOnTimeline = self.connection.statuses.home_timeline(count = toFind)
        maxRetweets = 0
        for i in range(0,toFind):
            if maxRetweets < tweetsOnTimeline[i]["retweet_count"]:
                tweet = tweetsOnTimeline[i]
                maxRetweets = tweetsOnTimeline[i]["retweet_count"]
        self.logFile.write('\n'+self.getDateTime()+"\tMost retweetet has "+str(maxRetweets["retweet_count"]))
        try:
            self.delay()
            self.connection.statuses.retweet(id=tweet["id"])
            self.logFile.write('\n'+self.getDateTime()+"\tThs tweet has been rewteeted")
        except Exception,e:
            self.logFile.write('\n'+self.getDateTime()+'\t'+str(e))
            return


