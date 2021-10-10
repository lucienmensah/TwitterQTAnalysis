import tweepy
from datetime import datetime
from pprint import pprint
import pandas as pd
import sys
import re
import matplotlib.pyplot as plt
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords, movie_reviews
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier


'''
This is version 1 of this project, which does the basics of what I want this overall project to acheive

This program is taking in Twitter data, looking for key words, and then presenting their screen name,
the tweet with the key word, and their bio. 

Next steps: figuring out how we can get the pronouns in their bio to be inclusive if they use other
pronouns. Right now, I am testing this out with three twitter accounts that are of two binary trans
people and a non-binary trans person. [done]
I need to see if I can query more than one phrase.
Need to use pandas to place this in a dataframe for neat presentation and analysis.

!!! important: This code is currently undergoing revision. It is currently inefficient and messy, but this was put
up on github because it does what it was meant to do, though it has areas that are redundant. !!!

Other words that incorporate the pronouns, neologisms based on pronouns
    before or after
    word longer than 5 letters including they and them
    
    people started w pronouns in their bios, expanded to create words
to include RT or to not........ maybe track seperately 

scrape the tweets and get bios from the tweeters

tracking pronouns, gender expression words, and thembo etc.  in tweets, looking for correlation
in people who use these wor ds in conjunction to being queer
only looking for people who use pronouns in their bio

do i need to tokenize the words? - not yet

look at levels of proximity, what's considered out group vs in group

comparing amounts of people that use more than two sets of pronouns
i want the specific word
look for new words
Add: 
    
Tweepy is only pulling 100 tweets. Need to figure out a way around this.
https://blog.finxter.com/how-to-match-an-exact-word-in-python-regex-answer-dont/
'''

consumer_key = " "
consumer_secret = " "
access_token = " "
access_token_secret = " "

#creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
#creating the API object while passing in auth information
api = tweepy.API(auth)

#account list for people we want to analyze
account_list = ['uwucien','notsumma','flowerhija','annaperng']
#this should be a function
if len(account_list) > 0:
  for target in account_list:
    item = api.get_user(target)
    twt_bio = item.description
    print("Getting data for " + target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("location: " + item.location)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
 
    
#looks within description, sees pronouns and flags for possible gender marker, reg ex is used to determine each marker
pronouns = 0
if re.search((r'\bhe\b' or r'\bhim\b'), twt_bio):
            print('! likely masc')
            pronouns = 1            
if re.search((r'\bshe\b' or r'\bher\b'), twt_bio):
             print('! possibily fem')
             pronouns = 1
if re.search((r'\bthey\b' or r'\bthem\b'), twt_bio): #any pronouns, all pronouns
            print("! possibly nb")
            pronouns = 1
'''
additional pronoun sets to search for: xe/xir, it/its, he/they ,she/they
'''         
            
if pronouns == 0:  # if there aren't pronouns in bio
        print("! no pronouns or neopronouns")
  

#pronouns = "she","her","him","his","they","them","bun","xe","xir" #figure out how to list multiple strings
      
#empty list for people who are possibly nonbinary (using that as a general catch all, will elaborate)

user_features_list = ["screen_name", "name", "location", "bio", "tweet",
                      "he/him", "she/her", "they/them",
                      "it/its", "xe/xem", "ze/zir"]

query_list = ["thembo","bimbo","himbo","theydies","ladies", "gentlethem", "gentlemen", "theybie", "transgender","transwoman","transman"]
res_dict = {} 

#english language tweets
language = "en"
#can set number of tweets to pull - up to 100
numTweets = 100
#calling the user_timeline function with our parameters
for query in query_list:
    res_dict[query] = api.search(q=query, lang=language, count=numTweets)

#needs to not matter if they use caps or not
#function to search through tweets
#def searchTweet(x):
for query in query_list:   
    users_df = pd.DataFrame(columns = user_features_list)
    pro_they = []
    pro_he = []
    pro_she = []
    pro_it = []
    pro_xe = []
    pro_ze = []
    no_pronouns = []
    authors = []
#no pronouns, but uses nb or genderqueer
    nbgq = []
    tweets = []
    for tweet in res_dict[query]: #there has to be a way to make this less redundant
        #prints the username, tweet w query, and bio description
        tweets.append(tweet.text)
        #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
        authors.append(tweet.user.screen_name)
        #this searches for they/them
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description, re.IGNORECASE):
            pro_they.append(tweet.user.screen_name) #searches for they/them
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.location, re.IGNORECASE):
            pro_they.append(tweet.user.screen_name) #searches for they/them
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description, re.IGNORECASE):
            pro_she.append(tweet.user.screen_name)
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.location, re.IGNORECASE):
            pro_she.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.description, re.IGNORECASE):
            pro_he.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.location, re.IGNORECASE):
            pro_he.append(tweet.user.screen_name)
        if re.search((r'\bit\b' or r'\bits\b'), tweet.user.description, re.IGNORECASE):
            pro_it.append(tweet.user.screen_name)
        if re.search((r'\bit\b' or r'\bits\b'), tweet.user.location, re.IGNORECASE):
            pro_it.append(tweet.user.screen_name)
        if re.search((r'\bxe\b' or r'\bxir\b' or r'\bxem\b' or r'\bxey\b'), tweet.user.description, re.IGNORECASE):
            pro_xe.append(tweet.user.screen_name)
        if re.search((r'\bxe\b' or r'\bxir\b' or r'\bxem\b' or r'\bxey\b'), tweet.user.location, re.IGNORECASE):
            pro_xe.append(tweet.user.screen_name)
        if re.search((r'\bze\b' or r'\bzir\b' or r'\bzem\b'), tweet.user.description, re.IGNORECASE):
            pro_ze.append(tweet.user.screen_name)
        if re.search((r'\bze\b' or r'\bzir\b' or r'\bzem\b'), tweet.user.location, re.IGNORECASE):
            pro_ze.append(tweet.user.screen_name)
            #de,dem
   #people who use words like genderqueer, nb
        if re.search((r'\bnonbinary\b' or r'\bgenderqueer\b'), tweet.user.description, re.IGNORECASE):
           nbgq.append(tweet.user.screen_name)
           
    for tweet in res_dict[query]: #this may not be necessary    
    # Create empty dict
        user_features = {}
    # Get user data
        user_features['bio'] = tweet.user.description
        user_features['screen_name'] = tweet.user.screen_name
        user_features['name'] = tweet.user.name
        user_features['tweet'] = tweet.text
        user_features['location'] = tweet.user.location
        #fills in the yeses
        if tweet.user.screen_name in pro_they:
            user_features['they/them'] = 'yes'
        if tweet.user.screen_name in pro_he:
            user_features['he/him'] = 'yes'
        if tweet.user.screen_name in pro_she:
            user_features['she/her'] = 'yes'
        if tweet.user.screen_name in pro_it:
            user_features['it/its'] = 'yes'
        if tweet.user.screen_name in pro_xe:
            user_features['xe/xem'] = 'yes'
        if tweet.user.screen_name in pro_ze:
            user_features['ze/zem'] = 'yes'
        #fills in the nos
        if tweet.user.screen_name not in pro_he:
            user_features['he/him'] = 'no'
        if tweet.user.screen_name not in pro_she:
            user_features['she/her'] = 'no'
        if tweet.user.screen_name not in pro_xe:
            user_features['xe/xem'] = 'no'
        if tweet.user.screen_name not in pro_they:
            user_features['they/them'] = 'no'
        if tweet.user.screen_name not in pro_it:
            user_features['it/its'] = 'no'
        if tweet.user.screen_name not in pro_ze:
            user_features['ze/zir'] = 'no'
        # concat the dfs
        user = pd.DataFrame(user_features, index = [0])
        users_df = pd.concat([users_df, user], ignore_index = True)
    date_string = '4_24'
    filename = '%s_%s.csv' % (query, date_string)   
    users_df.to_csv(filename, encoding='utf-8', index=False)
   # return pro_ze, pro_xe, pro_it, pro_he, pro_she, pro_they
# list of usernames
    pro = pro_ze + pro_xe + pro_it + pro_he + pro_she + pro_they
    print(query," length of set of pro: ", len(set(pro)))

screennames = []

#Track amount of people who use both nb and binary pronouns, right now only tracks 2
he_they = []
she_they = []
nb = []
tweets = []
multi = 0

# the code below should be done in a separate program which is the actual data analysis
# but, it currently exists here to explore the data, while running code
#total = len(set(pro_they)) + len(set(pro_she))+ len(set(pro_he)) + nopronouns + len(set(pro_it)) + len(set(pro_xe))+ len(set(pro_ze)) +len(set(he_they)) + len(set(she_they))
#percentage of people who do not have pronouns in their bios
#print("Percentage of people with no pronouns:", nopronouns / total)
#percentage of people who use she/her
print("Total number of pronoun users: ", len(set(pro)))
print("Percentage of people with she/her pronouns:", len(set(pro_she)) / len(set(pro)))
print("Number of people with she/her: ", len(set(pro_she)))
#percentage of people who use he/him
print("Percentage of people with he/him pronouns:", len(set(pro_he)) / len(set(pro)))
print("Number of people with he/him: ", len(set(pro_he)))
#percentage of people who use they/them
print("Percentage of people with they/them pronouns:", len(set(pro_they)) / len(set(pro)))
print("Number of people with they/them: ", len(set(pro_they)))
#percentage of people who use they/them
print("Percentage of people with it/its pronouns:", len(set(pro_it)) / len(set(pro)))
print("Number of people with it/its: ", len(set(pro_it)))
#percentage of people who use they/them
print("Percentage of people with xe/xir pronouns:", len(set(pro_xe)) / len(set(pro)))
print("Number of people with xe/xir: ", len(set(pro_xe)))
#percentage of people who use they/them
#print("Percentage of people with ze/zir pronouns:", len(set(pro_ze)) / len(set(pro))) 
#print("Number of people with ze/him: ", len(set(pro_he)))
#percentage of people who use he/they
print("Amount of people with both he and they pronouns: ", len(set(he_they)) / len(set(pro)))
print("Number of people with both he and they pronouns: ", len(set(he_they))) 
#percentage of people who use she/they
print("Amount of people with both she and they pronouns: ", len(set(she_they)) / len(set(pro)))
print("Number of people with both she and they pronouns: ", len(set(she_they))) 
      
    #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)          
#print("He/they: ", list(set(he_they)))
#print("She/they: ", list(set(she_they)))

#percentages of two sets of pronouns


#graph of thembo to theydie screen name ratio
#graph of thembo to theydie name (like display name) ratio

labels = ["she/her","they/them", 'he/him', 'it/its','xe/xem','he/they','she/they']
sizes = [(len(set(pro_she)) / len(set(pro))),(len(set(pro_they)) / len(set(pro))), (len(set(pro_he)) / len(set(pro))),(len(set(pro_it)) / len(set(pro))),(len(set(pro_xe)) / len(set(pro))),(len(set(he_they)) / len(set(pro))), (len(set(she_they)) / len(set(pro)))]
plt.pie(sizes, labels=labels,explode= (0.01,0.01,0.01,0.01,0.01,0.01,0.01,), autopct='%1.1f%%')
plt.axis('equal')
plt.show()


import time
# need to check which is the most useful - this or the code above
# create empty dataframe
user_features_list = ["screen_name", "name", "location", "bio", "tweet",
                      "he/him", "she/her", "they/them",
                      "it/its", "xe/xem", "ze/zir"]

users_df = pd.DataFrame(columns = user_features_list)
for query in query_list:
    for tweet in res_dict[query]:
    # create empty dict
        user_features = {}
    # Get user data
    #if user in pro:
   # item = api.get_user(user)
        user_features['bio'] = tweet.user.description
        user_features['screen_name'] = tweet.user.screen_name
        user_features['name'] = tweet.user.name
        user_features['tweet'] = tweet.text
        user_features['location'] = tweet.user.location
        #fills in the yeses
        if tweet.user.screen_name in pro_they:
            user_features['they/them'] = 'yes'
        if tweet.user.screen_name in pro_he:
            user_features['he/him'] = 'yes'
        if tweet.user.screen_name in pro_she:
            user_features['she/her'] = 'yes'
        if tweet.user.screen_name in pro_it:
            user_features['it/its'] = 'yes'
        if tweet.user.screen_name in pro_xe:
            user_features['xe/xem'] = 'yes'
        if tweet.user.screen_name in pro_ze:
            user_features['ze/zem'] = 'yes'
        #fills in the nos
        if tweet.user.screen_name not in pro_he:
            user_features['he/him'] = 'no'
        if tweet.user.screen_name not in pro_she:
            user_features['she/her'] = 'no'
        if tweet.user.screen_name not in pro_xe:
            user_features['xe/xem'] = 'no'
        if tweet.user.screen_name not in pro_they:
            user_features['they/them'] = 'no'
        if tweet.user.screen_name not in pro_it:
            user_features['it/its'] = 'no'
        if tweet.user.screen_name not in pro_ze:
            user_features['ze/zir'] = 'no'
        # Concat the dfs
        user = pd.DataFrame(user_features, index = [0])
        users_df = pd.concat([users_df, user], ignore_index = True)
        date_string = '4_18'
        filename = '%s_%s.csv' % (query, date_string)
        
        users_df.to_csv((query, date_string), encoding='utf-8', index=False)
#        return users_df

'''
in my dataframe i want:
    title is: which search results they appeared from
    tweet (to tokenize for ngrams)
    user.screen_name
    user.description
    their pronouns
    if they use two sets of pronouns
'''   