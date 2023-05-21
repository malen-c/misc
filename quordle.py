import re
from random import sample
from math import prod, log2
from collections import Counter
import numpy as np

with open('words.txt', 'r') as fob:
    guesses = [x for x in fob.read().splitlines() if re.fullmatch(r'[a-z]{5}', x)]

with open('answers.txt', 'r') as fob:
    answers = fob.read().splitlines()


def compatible(g, t):
    # Returns list of target words that are still possible after guess is made
    possible_answers = answers
    check = {x: True for x in range(5)}
    # GREEN
    for i in check:
        if g[i] == t[i]:
            possible_answers = [p for p in possible_answers if g[i] == p[i]]
            check[i] = False
    # YELLOW
    for i in check:
        if check[i] and g[i] in t:
            possible_answers = [p for p in possible_answers if g[i] in p]
            check[i] = False
    # GREY
    for i in check:
        if check[i]:
            possible_answers = [p for p in possible_answers if g[i] not in p]

    # REPEATED LETTERS
    cg = [x for x in Counter(g).items() if x[1] > 1]
    ct = [x for x in Counter(t).items() if x[1] > 1]
    if len(cg) > 0 and len(ct) > 0:
        for gletter, gcount in cg:
            for tletter, tcount in ct:
                if gletter == tletter:
                    mincount = min(gcount, tcount)
                    possible_answers = [p for p in possible_answers if Counter(p)[gletter] >= mincount]
    return possible_answers


class Game:
    def __init__(self):
        # Select 4 random words to be the answers for this game
        self.targets = sample(answers, 1)
        self.n_possible = [len(answers)] * 1

    def guess(self, g):
        # Enter a guess; method automatically checks which words are no longer possible
        # for each target word based on hints returned
        for i, t in enumerate(self.targets):
            self.n_possible[i] = len(compatible(g, t))

    def info(self):
        return -log2(prod(self.n_possible)/len(answers)**1)


results = [0] * len(guesses)

x = Game()
for i in range(len(guesses)):
    x.guess(guesses[i])
    results[i] += x.info()

mean = np.mean(results)
sd = np.var(results)**.5

# Only check words with info better than mean minus 1.5 SDs
check = [i for i in range(len(guesses)) if results[i] > mean - 1.5 * sd]

while len(check) > 50:
    x = Game()
    for i in check:
        x.guess(guesses[i])
        results[i] += x.info()
    mean = np.mean([results[i] for i in check])
    sd = np.var([results[i] for i in check])**.5

    # Increase stringency as repetitions increase
    check = [i for i in check if results[i] > mean - (len(check)/len(guesses) * sd)]
    print(len(check))

print(np.array(guesses)[sorted(check, key=lambda x: results[x], reverse=True)])
