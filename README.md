# BotNet Classifier:

Quick and simple Binary Classifier to determine if the tweets are from a Bot or Human using Dynamic Time warping as co-relation coeffecient and supervised learning for classification for CS 221 Project.

Correlation function uses the following features:

##### Tweet:
- Text
- Timestamp

### Results on Test Data
**Sample Size:**
Training Data : ~140K tweets
Test Data : ~200K tweets

| Category | Success Rate |
| ------ | ------ |
| True Positive | 62.49% |
| False Positive | 26.07% |
| Unknown( includes False Positive) | 11.6% |
| True Negative | 26.45% |

**Total Success rate: 88.94%**

### Running the code

```sh
$ python cluster_users.py
```

### Data Courtesy:
https://botometer.iuni.iu.edu/bot-repository/datasets.html

### Contributors:
 - Ananth Rao
 - Ashwin Neerabail
- Yatharth Agarwal