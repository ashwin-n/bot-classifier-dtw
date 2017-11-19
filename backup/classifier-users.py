#!/usr/bin/python
import random
from  collections import defaultdict
from collections import Counter
import math
import sys
from utils import *

def extractUserFeatures(tokens):
    fields = readFields('../data/metadata/fields-users.train')
    phi = defaultdict(float)
    for index, fieldValue in enumerate(tokens):
        sanitizedFieldName = fields[index].replace('"','')
        if sanitizedFieldName in ['statuses_count','followers_count','friends_count','favourites_count','default_profile','default_profile_image','follow_request_sent','contributors_enabled','following']:
        # if index ==1:
            sanitizedFieldValue = fieldValue.strip()
            if sanitizedFieldValue not in ["","NULL","...","&amp;","-","."]:
                # if sanitizedFieldName in ['statuses_count','followers_count','friends_count','favourites_count']:
                #     count = int(fieldValue)
                #     phi[sanitizedFieldName+] +=  1
                    # if count == 0:
                    #     phi[sanitizedFieldName+':0'] +=  1
                    # elif count >0 and count<2:
                    #     phi[sanitizedFieldName+':1-2'] +=  1
                    # elif count>10:
                    #     phi[sanitizedFieldName+': >10'] +=  1
                # else:
                phi[sanitizedFieldName+':'+fieldValue] +=  1
                
            #     # for tweetWord in tweet:
            #     #     phi[fields[index]+"split"+tweetWord] +=  1
            #     input = word.replace(" ", "")
            #     input = input.replace("\t", "")
            #     for i in range(len(input)-4+1):
            #             phi[fields[index]+"split"+input[i:i+4]] += 1

    return phi

def learnPredictor(trainExamples, featureExtractor, numIters, eta):
    weights = {}
    trainExamples_extracted = []
    print "Extracting features"
    for x, y in trainExamples:
        trainExamples_extracted.append((featureExtractor(x), y))
    print "Done extracting features"
    for t in range(numIters):
        for (phi, y) in trainExamples_extracted:
            if(1 - dotProduct(weights, phi) * y > 0):#max(0, 1-dot(weights, phi))
                increment(weights, eta * y, phi)#Stochastic Gradient Descent ; gradient is -phi*y  , w = w - eta* -phi.y = w+(eta*y).phi
        trainError = evaluatePredictor(trainExamples_extracted, lambda(x) : (1 if dotProduct(x, weights) >= 0 else -1))
        print "Iteration = %d, Train error = %f" %(t , trainError)
    # END_YOUR_CODE
    return weights


trainExamples = readExamples('../data/users-bots.train','../data/users-genuine.train')
random.shuffle(trainExamples)
featureExtractor = extractUserFeatures
weights = learnPredictor(trainExamples, featureExtractor, numIters=20, eta=0.01)
print "Done training"
outputWeights(weights, 'weights')

# trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
testExamples = readExamples('../data/users-bots.test','../data/users-genuine.test')
random.shuffle(testExamples)
testError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
outputErrorAnalysis(testExamples, featureExtractor, weights, 'error-analysis')  # Use this to debug
print "Official: test error = %s" % (testError)