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
        return dict( [(x.strip().split(',')[0], (x.strip().split(',')[1], x.strip().split(',')[2])) for x in content ])
    else:
        return dict([ tuple(x.strip().split(',')) for x in content ])


obscenities = loadDictionary('obscenities')
slogans = loadDictionary('slogans')
amplifiers = loadDictionary('amplifiers')

#Gets the slogan
#@Param: tweet text
#Return: tuple --> (slogan weight, plus how many slogans there are)
def removeTargetDuplicates(body, target, list=None):
    if list == None:
        return body.replace(target, '')


def sloganWeight(text):
    sloganWeights = []
    for slogan in slogans:
        if slogan in text:
            sloganWeights.append((100, text.count(slogan)))
            text.replace(text, '')
    return tuple(map(sum, zip(*sloganWeights)))

def obscenityWeight(textList, amplifier=None):
    return [obscenities[token] for token in textList if token in obscenities.keys()]

def amplifierWeight(text):
    return
#Normalizes the text by stripping it of any emojis or non-alphanumeric characters
#@Param: text to be normalized
#@Return: list --> [normalized text tokes]
def normalize(text):
    normalizedText = text
    if '\n' in text:
        normalizedText = normalizedText.replace('\n', ' ')
    return re.sub('[^A-Za-z 0-9]+', '', normalizedText).split(' ')

#Performs the obscenity ranking
#@Param: text to be ranked in obscenity
#@Return: the ranking in obscenity of the text
punctuation = ['.', '!', '?', ',', '\'', '\\']
def rankText(text, slogans=None, amplifiers=None):
    sWeights = (0,0)
    aWeights = 0
    tWeights = 0

    if slogans != None:
        sWeights = sloganWeight(text)
    tokens = normalize(text)
    return obscenityWeight(tokens)





#print(rankText('dick ass fuck'))
#print(rankText('I\'m so fucking mad right now. I need help'))
#print(rankText('fuck the broncos, they can suck a dick'))
#print(rankText('Fuck trump man, nigga is gay af'))
#print(rankText('Did you cum in me!? Fuck you did huh you know what FUCK YOU fuck you fuck you, you fucking asshole.'))
#alaskan pipeline
#d = dict([('sexy','')])
#print('s' in d.itervalues())
d = time.time()
rankText('ass wipe black cock black cock', True, True)
print(time.time() - d)
