# -*- coding: utf-8 -*-

#A library used to detect obscenity, though in a very minimal and primative manner
import difflib
import re
import time
import math
import collections

#Loads the obscenity dictionary from the directory

def splitter(term):
    final = term.split(',')
    return (final[0], (float(final[1]), final[2]))

def loadDictionary(dictionary):
    content = ''
    with open('./dictionaries/' + dictionary + '.txt') as d:
        content = d.readlines()
    if dictionary == 'obscenities':
        return dict( [(x.strip().split(',')[0], (x.strip().split(',')[1], x.strip().split(',')[1])) for x in content ])
    else:
        return dict([ tuple(x.strip().split(',')) for x in content ])


obscenities = loadDictionary('obscenities')
slogans = loadDictionary('slogans')
amplifiers = loadDictionary('amplifiers')
#slogans = dict(slogans)
#Gets the slogan
#@Param: tweet text
#Return: tuple --> (slogan ranking, plus how many slogans there are)
def sloganWeight(text):
    sloganWeights = []
    for slogan in slogans:
        if slogan in text:
            sloganWeights.append((100, text.count(slogan)))
    return map(sum, zip(*sloganWeights))



#Performs the obscenity ranking
#@Param: text to be ranked in obscenity
#@Return: the ranking in obscenity of the text
punctuation = ['.', '!', '?', ',', '\'', '\\']
def rankText(text, slogans, amplifiers):
    sWeights = 0
    aWeights = 0
    tWeights = 0

    tokens = re.sub('[^A-Za-z 0-9]+', '', text).split(' ')
    matches = [(token, closeMatches(token)) for token in tokens if closeMatches(token)]
    if len(matches) == 0:
        return 0.0
    #This needs explanation. Essentially this takes the matched terms and puts them in a list (inner list comprehension)
    #There are possible sublists in the list, where the outer list comprehension flattens the elements to be only individual
    refinedMatches = [match for sublist in [confirmObscene(term) for term in matches if confirmObscene(term)] for match in sublist]
    if len(refinedMatches) == 0:
        return 0.0
    termRankList = list(map(lambda word: dict(dictionary)[word], refinedMatches))
    frequencySum = list(map(lambda freq: float(freq), dict(collections.Counter(refinedMatches)).values()))
    weight = [float(term[0]) for term in termRankList]

#print(rankText('dick ass fuck'))
#print(rankText('I\'m so fucking mad right now. I need help'))
#print(rankText('fuck the broncos, they can suck a dick'))
#print(rankText('Fuck trump man, nigga is gay af'))
#print(rankText('Did you cum in me!? Fuck you did huh you know what FUCK YOU fuck you fuck you, you fucking asshole.'))
#alaskan pipeline
#d = dict([('sexy','')])
#print('s' in d.itervalues())

print sloganWeight('ass wipe black cock black cock')
