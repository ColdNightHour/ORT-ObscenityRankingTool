# -*- coding: utf-8 -*-

#A library used to detect obscenity, though in a very minimal and primative manner
import re
import math
import collections
#Loads the obscenity dictionary from the directory

#Loads a text list into a dictionary
#@Param: A text file of terms
#@Return: dict --> {dictionary of terms}
def loadDictionary(path):
    content = ''
    with open(path) as d:
        content = d.readlines()
    if path.find('obscenities.txt') != -1:
        return dict( [(x.strip().split(',')[0], (float(x.strip().split(',')[1]), len(x.strip().split(',')[2]))) for x in content ])
    else:
        return dict([ tuple(x.strip().split(',')) for x in content ])

#Calls the loadDictionary function to populate the three dictionaries
obscenities = loadDictionary('/home/jadixon/Documents/PyORT/dictionaries/obscenities.txt')
slogans = loadDictionary('/home/jadixon/Documents/PyORT/dictionaries/slogans.txt')
amplifiers = loadDictionary('/home/jadixon/Documents/PyORT/dictionaries/amplifiers.txt')



def sloganWeight(text):
    sloganWeights = 0
    amtSlogans = 0
    contributions = 0;

    for slogan in slogans or slogan.replace(' ','') in text:
        if slogan in text:
            index = text.find(slogan)
            actual = text[index:index+len(slogan)+1 if index+len(slogan)+1 <= len(text) else len(text)]
            if actual == (slogan + ' '):
                sloganWeights = sloganWeights + 100
                contributions = contributions + len(slogan.split(' '))
                amtSlogans = amtSlogans + 1
    return (sloganWeights*amtSlogans + 1, contributions)

#Counts the amount of amplifiers in the text
#@Param: text to be analyzed
#@Return: Integer --> Number of amplifiers
def amplifierWeight(textList, ampPerWord):
    if ampPerWord == 0:
        return (1, 0)
    ampCount = len(['multiplier' for token in textList if token in amplifiers.keys()])
    return (10*ampPerWord*ampCount + 1, ampCount)

def obscenityWeight(textList):
    scores = [(obscenities[token][0], obscenities[token][1]) for token in textList if token in obscenities.keys()] #A list comprehension to make a list of values
    ampPerWord = 0;
    obscenityWeight = 0
    amtObscenities = 0

    for score in scores:
        obscenityWeight = obscenityWeight + float(score[0])
        ampPerWord = ampPerWord + score[1]
        amtObscenities = amtObscenities + 1

    return (obscenityWeight*amtObscenities + 1, amtObscenities, ampPerWord)

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
def rankLineText(text, slogans=True, amplifiers=True, externalAffect=False):
    sWeights = (1,0)
    oWeights = (1,0)
    aWeights = (1,0)

    if slogans != None:
        sWeights = sloganWeight(text)

    tokens = normalize(text)
    oWeights = obscenityWeight(tokens)

    if amplifiers != None:
        aWeights = amplifierWeight(tokens, oWeights[2])

    contributions = math.pow((sWeights[1] + oWeights[1] + aWeights[1]) + 1, 2)
    nonContributions = len(tokens) - (sWeights[1] + oWeights[1] + aWeights[1]) + 1

    #print aWeights
    #print sWeights
    #print oWeights

    if nonContributions == 0 or oWeights[0] == 1:
        nonContributions = 1
    if not externalAffect:
        return math.log(aWeights[0]*oWeights[0]*sWeights[0]*contributions*1/nonContributions, 10)
    elif externalAffect:
        return math.log((aWeights[0]*oWeights[0]*sWeights[0]*contributions*1/nonContributions + 1)*100, 10)

def rankDocument(document):
    documentSplit = document.split('\n')
    globalObscenity = []
    relativeObscenity = []
    for document in documentSplit:
        score = rankLineText(document)
        if score != 0.0:
            relativeObscenity.append(score)
        globalObscenity.append(score)
    return (sum(globalObscenity)/len(globalObscenity), sum(relativeObscenity)/len(relativeObscenity))
