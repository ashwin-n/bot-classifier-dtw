import sys
import csv
from utils import *
reload(sys)
sys.setdefaultencoding('utf8')

with open('results.csv') as fin:
    correct = 0
    wrong = 0 
    falsePositive =0
    falseNegative=0
    trueNegative =0
    for line in fin:
        # print line.split(",")[6], line.split(",")[6]
        result = line.split(",")[7].strip()
        if result=='TRUE':
            correct+=1
        else:
            wrong+=1
        if (line.split(",")[1].strip() =='0' or line.split(",")[3].strip() =='0') and line.split(",")[5].strip() =='TRUE':
           falsePositive+=1 
        if line.split(",")[4].strip() !='inf' and line.split(",")[5].strip() =='FALSE' and line.split(",")[6].strip() =='TRUE':
            falseNegative+=1
        if (line.split(",")[1].strip() =='0' or  line.split(",")[3].strip() ==0) and line.split(",")[5].strip() =='FALSE':
            trueNegative+=1   
    total = correct+wrong    
    print "falsePositive:{}".format(float(falsePositive)/total)
    print "falseNegative:{}".format(float(falseNegative)/total)
    print "trueNegative:{}".format(float(trueNegative)/total)
    print "truePositive:{}".format(float(correct)/total)

