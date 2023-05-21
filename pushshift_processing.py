import ijson
import pandas as pd
import re

# Reads in archived reddit comments acquired from pushshift.io, which must be opened as a stream since they're so large.
# This was data collection for a linguistics research project on changes in use of the novel term "normie" on Reddit
# over time.

f = open('RC_2017-12', 'rb')
parser = ijson.parse(f, multiple_values=True)

n = 100000

# body, created_utc, score, subreddit
body = ['']*n
controversiality = [0]*n
created_utc = [0]*n
score = [0]*n
subreddit = ['']*n

lists = {'subreddit': subreddit,
         'created_utc': created_utc,
         'body': body,
         'score': score,
         'controversiality': controversiality
}

i = 0



try:
    while i < n:
        prefix, event, value = next(parser)
        if event == 'end_map' and re.search('[nN][oO][rR][mM][iI][eE]', body[i]):
            i += 1
        if prefix in lists:
            lists[prefix][i] = value
except StopIteration:
    print('stop iteration')

df = pd.DataFrame.from_dict(lists).drop_duplicates()
df = df.drop([df.shape[0]-2, df.shape[0]-1], axis=0)
df.to_excel('c:/users/malen/desktop/2017.xlsx', index_label=False)
