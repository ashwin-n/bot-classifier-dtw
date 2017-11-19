import os, random, operator, sys
from collections import Counter
import csv
import codecs

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def readFields(labelPath):
    for line in open(labelPath):
        words = line.split(',')
    return words

def csv_read(csv_reader): 
    while True: 
        try: 
            yield next(csv_reader) 
        except csv.Error:         
            pass
        continue 
    return

def getUserData():
    users1 = readUsers('data/users-bots.csv')
    users2 = readUsers('data/users-genuine.csv')
    users3 = readUsers('data/users-social-bots.csv')
    users = users1.copy()
    users.update(users2)
    users.update(users3)
    return users

def readUsers(userPath):
    users = {}
    for line in csv_read(csv.reader(open(userPath))):
        userId = line[0]
        users[userId]=line
    return users

def readTweets(path):
    examples = []
    for line in csv_read(csv.reader(open(path))):
        examples.append(line)
    print 'Read %d examples from %s' % (len(examples), path)
    random.shuffle(examples)
    return examples

def readExamples(positivePath, negativePath):
    examples = []
    for line in csv_read(csv.reader(open(positivePath))):
        examples.append((line, -1))
    for line in csv_read(csv.reader(open(negativePath))):
        examples.append((line, 1))
    print 'Read %d examples from %s and %s' % (len(examples), positivePath, negativePath)
    random.shuffle(examples)
    return examples

def evaluatePredictor(examples, predictor):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    falsePositive = 0
    falseNegative = 0
    trueNegative = 0
    truePositive = 0
    totalPositive = 0
    totalNegative = 0
    for x, y in examples:
        calculated = predictor(x)
        if y ==1:
            totalPositive+=1
        if y ==0:
            totalNegative+=1
        if  calculated!= y:
            error += 1
        if calculated == 1 and y ==1:
            truePositive+=1
        if calculated == 0 and y ==0:
            trueNegative+=1
        if calculated == 0 and y ==1:
            falseNegative+=1
        if calculated == 1 and y ==0:
            falsePositive+=1
    print "totalPositive:{}, totalNegative:{}".format( 1.0 *totalPositive/ len(examples),1.0 *totalNegative/ len(examples))
    print "falsePositive:{}, falseNegative:{},trueNegative:{},truePositive:{}".format( 1.0 *falsePositive/ len(examples),1.0 *falseNegative/ len(examples),1.0 *trueNegative/ len(examples),1.0 *truePositive/ len(examples))
    return 1.0 * error / len(examples)

def outputWeights(weights, path):
    print "%d weights" % len(weights)
    out = open(path, 'w')
    for f, v in sorted(weights.items(), key=lambda (f, v) : -v):
        print >>out, '\t'.join([str(f), str(v)])
    out.close()

def verbosePredict(phi, y, weights, out):
    yy = 1 if dotProduct(phi, weights) >= 0 else -1
    if y:
        print >>out, 'Truth: %s, Prediction: %s [%s]' % (y, yy, 'CORRECT' if y == yy else 'WRONG')
    else:
        print >>out, 'Prediction:', yy
    for f, v in sorted(phi.items(), key=lambda (f, v) : -v * weights.get(f, 0)):
        w = weights.get(f, 0)
        print >>out, "%-30s%s * %s = %s" % (f, v, w, v * w)
    return yy

def outputErrorAnalysis(examples, featureExtractor, weights, path):
    out = open('error-analysis', 'w')
    for x, y in examples:
        print >>out, '===', x
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()
