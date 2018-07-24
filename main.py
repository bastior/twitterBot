from bot import *
import datetime


myBot = Bot()

myBot.connect()

#myBot.tweet("Hello2")
#myBot.getFollowers()
#myBot.getFollowed()
#myBot.getTweetsByPhrase("madrid",10,"recent")

#myBot.autoRefollow()

#myBot.autoFollowFollowersOfUser("CNN")

#myBot.unfollowUsersNonFollowU()

#23424923 - Polska
#1 - Caly swiat
#753692 - Barcelona

#myBot.getTrendsByLocation(753692)


myBot.retweetByPhrase("Barcelona", 2, "recent")
#myBot.MostFollowFromFollowed()
#myBot.retweetMostPopular()
