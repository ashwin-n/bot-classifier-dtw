import sys
import csv
from utils import *
reload(sys)
sys.setdefaultencoding('utf8')

with open('data/tweets-social-bots-full.csv') as fin:
        with open('data/tweets-social-bots.final', 'w') as fout1:
            i = 0
            j=0
            for line in fin:
                line = unicode(line, errors='ignore')
                print i
                if (i >110000 and i<200000) or i <30000:
                    j=j+1
                    fout1.write(line)
                    i+=1
                else:
                    if i<200000:
                        i+=1
                    else:
                        break
            print j

# with open('data/tweets-genuine-users-full.csv') as fin:
#         with open('data/tweets-genuine.test', 'w') as fout1:
#             i = 0
#             for line in fin:
#                 line = unicode(line, errors='ignore')
#                 if i <80000:
#                     try:
#                         fout1.write(line)
#                     except IndexError:
#                         pass
#                     i+=1
#                 else:
#                     break
