#!/usr/bin/python
import random
from  collections import defaultdict
from  collections import OrderedDict
from collections import Counter
import math
import sys
from utils import *
import datetime
import hashlib

users = getUserData()


def mapUserToBot(testExamples, isBot):
    userBotMap = {}
    field_Tweets = readFields('data/metadata/fields-tweet.train')
    field_Users = readFields('data/metadata/fields-users.train')
    userIndex = 0
    for index , fieldValue in enumerate(field_Tweets):
        sanitizedFieldName = fieldValue.replace('"','')
        if 'user_id' == sanitizedFieldName:
            userIndex = index

    for tweet in testExamples:
        userId =  tweet[userIndex]
        userBotMap[userId] = isBot
    return userBotMap

def extractTweetFeatures(testExamples):
    field_Tweets = readFields('data/metadata/fields-tweet.train')
    field_Users = readFields('data/metadata/fields-users.train')

    user_to_tweetTime = {}
    user_to_tweet = {}
    userFieldValue = 'user_id'
    timeFieldValue ='timestamp'
    tweetFieldValue = 'text'
    userIndex = 0
    timeIndex = 0
    tweetIndex = 0

    for index , fieldValue in enumerate(field_Tweets):
        sanitizedFieldName = fieldValue.replace('"','')
        if userFieldValue == sanitizedFieldName:
            userIndex = index
        if timeFieldValue  == sanitizedFieldName:
            timeIndex = index
        if tweetFieldValue  == sanitizedFieldName:
            tweetIndex = index
    

    for tweet in testExamples:
        userId =  tweet[userIndex]
        tweetTime =  tweet[timeIndex]
        tweetText = tweet[tweetIndex]

        tweetHash = hashlib.md5(tweetText).hexdigest()
        
        if userId not in user_to_tweetTime:
            user_to_tweetTime[userId]=[]
        user_to_tweetTime[userId].append((tweetHash, convertToEpoch(tweetTime), tweetTime, tweetText))

        if userId not in user_to_tweet:
            user_to_tweet[userId]=[]
        user_to_tweet[userId].append(tweetHash)


    return user_to_tweetTime, user_to_tweet

def convertToEpoch(str):
    arr = []
    dateAndTime = str.split(" ")
    arr.extend(dateAndTime[0].split("-"))
    arr.extend(dateAndTime[1].split(":"))
    timeAsInt = [int(str) for str in arr]
    return datetime.datetime(*timeAsInt).strftime('%s')

def DTWDistance(s1, s2,w):
    DTW={}
    w = max(w, abs(len(s1)-len(s2)))

    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return math.sqrt(DTW[len(s1)-1, len(s2)-1])

def correlationFeatureExtractor(factor):
    phi = defaultdict(float)
    buckets = []
    for i in range(100000,999000000, 100000):
        buckets.append((10000, i+10000))
    if factor == float("inf"):
        phi['inf'] +=1
    else:
        for low, high in buckets:
            if factor >low and factor <high:
                phi[high]+=1
                break
    return phi


def learnPredictor(trainExamples, featureExtractor, numIters, eta):
    weights = {}
    trainExamples_extracted = []
    print "Extracting features"
    for x, y in trainExamples:
        trainExamples_extracted.append((featureExtractor(x), y))
    print "Done extracting features", len(trainExamples_extracted)
    print trainExamples_extracted
    for t in range(numIters):
        for (phi, y) in trainExamples_extracted:
            if(1 - dotProduct(weights, phi) * y > 0):#max(0, 1-dot(weights, phi))
                increment(weights, eta * y, phi)#Stochastic Gradient Descent ; gradient is -phi*y  , w = w - eta* -phi.y = w+(eta*y).phi
        trainError = evaluatePredictor(trainExamples_extracted, lambda(x) : (1 if dotProduct(x, weights) >= 0 else -1))
        print "Iteration = %d, Train error = %f" %(t , trainError)
    # END_YOUR_CODE
    return weights

botExamples = readTweets('data/tweets-social-bots.train')
genuineExamples = readTweets('data/tweets-genuine.train')

botTestExamples = readTweets('data/tweets-social-bots.test')
genuineTestExamples = readTweets('data/tweets-genuine.test')

userBotMap = mapUserToBot(botExamples, 1)
userBotMap.update(mapUserToBot(genuineExamples, 0))
userBotMap.update(mapUserToBot(botTestExamples, 1))
userBotMap.update(mapUserToBot(genuineTestExamples, 0))


def getCorrelation(allExamples):
    user_to_tweetTime, user_to_tweet =  extractTweetFeatures(allExamples)

    user_to_commmonTweetTime ={}
    trainExamples=[]


    for user1 in user_to_tweet:
        for user2 in user_to_tweet:
            if user1 != user2:
                tweetsForUser1 = user_to_tweet[user1]
                tweetsForUser2 = user_to_tweet[user2]
                commonTweets = list(set(tweetsForUser1).intersection(tweetsForUser2))
                if len(commonTweets) >0 :
                    user_to_commmonTweetTime[user1]=[]
                    commonTweetsSubset = commonTweets[:20]
                    for (tweetHash, tweetTime, tweetTimeHR, tText) in user_to_tweetTime[user1]:
                        if tweetHash in commonTweetsSubset:
                            # print tweetHash, tText, tweetTimeHR
                            user_to_commmonTweetTime[user1].append(int(tweetTime))
                    user_to_commmonTweetTime[user1]=list(set(user_to_commmonTweetTime[user1]))
                    user_to_commmonTweetTime[user2]=[]
                    for (tweetHash, tweetTime, tweetTimeHR, tText) in user_to_tweetTime[user2]:
                        if tweetHash in commonTweetsSubset:
                            # print tweetHash, tText, tweetTimeHR
                            user_to_commmonTweetTime[user2].append(int(tweetTime))
                    user_to_commmonTweetTime[user2]=list(set(user_to_commmonTweetTime[user2]))
                    user_to_commmonTweetTime[user1].sort()
                    user_to_commmonTweetTime[user2].sort()
                    dtw = DTWDistance(user_to_commmonTweetTime[user1], user_to_commmonTweetTime[user2], 0)
                    # if dtw != float("inf"):
                        #print user1 ,userBotMap[user1],  user2, userBotMap[user2], len(commonTweets), dtw/len(commonTweetsSubset)
                    classify =0
                    if userBotMap[user1] and userBotMap[user2]:
                        classify=1
                    if dtw != float("inf"):
                        trainExamples.append((dtw, classify))
                    print user1 ,userBotMap[user1],  user2, userBotMap[user2], dtw/len(commonTweetsSubset)        
                else:
                    print user1 ,userBotMap[user1],  user2, userBotMap[user2], 'inf'          
    return trainExamples


allExamples = botExamples + genuineExamples
trainExamples = getCorrelation(allExamples)

weights = learnPredictor(trainExamples,correlationFeatureExtractor, 20 ,0.1 )
orderedWeights = OrderedDict(sorted(weights.items()))

outputWeights(orderedWeights, 'weights')
allTestExamples = botTestExamples + genuineTestExamples
testExamples = getCorrelation(allTestExamples)

testError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(correlationFeatureExtractor(x), weights) >= 0 else -1))
print "Official: test error = %s" % (testError)
outputErrorAnalysis(testExamples, correlationFeatureExtractor, weights, 'error-analysis')  # Use this to debug


