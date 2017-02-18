# -*- coding: utf-8 -*-

#A library used to detect obscenity, though in a very minimal and primative manner
import difflib
import re
import time
import math
import collections

#Loads the obscenity dictionary from the directory

#Loads a text list into a dictionary
#@Param: A text file of terms
#@Return: dict --> {dictionary of terms}
def loadDictionary(dictionary):
    content = ''
    with open('./dictionaries/' + dictionary + '.txt') as d:
        content = d.readlines()
    if dictionary == 'obscenities':
        return dict( [(x.strip().split(',')[0], (float(x.strip().split(',')[1]), len(x.strip().split(',')[2]))) for x in content ])
    else:
        return dict([ tuple(x.strip().split(',')) for x in content ])

#Calls the loadDictionary function to populate the three dictionaries
obscenities = loadDictionary('obscenities')
slogans = loadDictionary('slogans')
amplifiers = loadDictionary('amplifiers')



def sloganWeight(text):
    sloganWeights = 0
    amtSloganWeights = 0
    contributions = 0;
    for slogan in slogans:
        if slogan in text:
            sloganWeights = sloganWeights + 100
            contributions = contributions + len(slogan.split(' '))
            amtSloganWeights = amtSloganWeights + 1
    if amtSloganWeights == 0:
        return (1,0)
    return (sloganWeights*(amtSloganWeights + 1), contributions)

#Counts the amount of amplifiers in the text
#@Param: text to be analyzed
#@Return: Integer --> Number of amplifiers
def amplifierWeight(textList, multPerWord):
    m = ['multiplier' for token in textList if token in amplifiers.keys()]
    if len(m) == 0 or multPerWord == 0:
        return (1, 0)
    multipliers = {'multiplier' : m.count(mult) for mult in m}
    return ((multPerWord*10*multipliers['multiplier'])*(multipliers['multiplier'] + 1), multipliers['multiplier'])

def obscenityWeight(textList):
    scores = [(obscenities[token][0], obscenities[token][1]) for token in textList if token in obscenities.keys()] #A list comprehension to make a list of values

    #print scores
    multPerWord = 0;
    obscenityWeight = 0
    amtObscenityWeights = 0

    for score in scores:
        obscenityWeight = obscenityWeight + float(score[0])
        multPerWord = multPerWord + score[1]
        amtObscenityWeights = amtObscenityWeights + 1
    if amtObscenityWeights == 0:
        return (1, 0, 0)
    return (obscenityWeight*(amtObscenityWeights + 1), amtObscenityWeights, multPerWord)

#Normalizes the text by stripping it of any emojis or non-alphanumeric characters
#@Param: text to be normalized
#@Return: list --> [normalized text tokes]
def normalize(text):
    normalizedText = text.lower()
    if '\n' in text:
        normalizedText = normalizedText.replace('\n', ' ')
    return re.sub('[^A-Za-z 0-9]+', '', normalizedText).split(' ')

#Performs the obscenity ranking
#@Param: text to be ranked in obscenity
#@Return: the ranking in obscenity of the text
punctuation = ['.', '!', '?', ',', '\'', '\\']
def rankText(text, slogans=True, amplifiers=True):
    sWeights = (1,0)
    oWeights = (1,0)
    aWeights = (1,0)

    if slogans != None:
        sWeights = sloganWeight(text)

    tokens = normalize(text)
    oWeights = obscenityWeight(tokens)

    if amplifiers != None:
        aWeights = amplifierWeight(tokens, oWeights[2])
    print oWeights
    print aWeights
    print sWeights

    contRatio = (sWeights[1] + oWeights[1] + aWeights[1])
    contRatio = ((contRatio * contRatio) / math.fabs(contRatio - len(tokens) + 1) + 1)
    return math.log(aWeights[0]*oWeights[0]*sWeights[0]*contRatio, 10)



d = time.time()
print(rankText('what a splendid day. I can\'t wait to see my love'))
print('\n')
#print(rankText('dick ass fuck'))
#print('\n')
#print rankText('long dick in my ass fuck')
#print('\n')
#print(rankText('I\'m so fucking mad right now. I need help'))
#print('\n')
#print rankText('sexy little lady, god damn')
#print('\n')
print(rankText('fuck the broncos'))
print('\n')
print(rankText('Fuck trump man, nigga is gay af'))
print('\n')
print(rankText('Nudity is the way to go SON'))
print('\n')
#print(rankText('Did you cum in me!? Fuck you did huh you know what FUCK YOU fuck you fuck you, you fucking asshole.'))
#print('\n')
print(time.time() - d)
