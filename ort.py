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
    return [ x.strip() for x in content ]


obscenities = loadDictionary('obscenities')
slogans = loadDictionary('slogans')
amplifiers = loadDictionary('amplifiers')

#Gets the slogan
#@Param: tweet text
#Return: tuple --> (slogan ranking, plus how many slogans there are)
def sloganWeight(text):
    print slogans
    slogansWeights = [100 for slogan_ in slogans if slogan_ in text]
    return (len(slogansWeights), sum(slogansWeights))

#Gets the close matches of a word
#@Param: word to be analyzed
#@Return: a sequence of obscene words that re best matches
def closeMatches(word):
    return difflib.get_close_matches(word, list(map(lambda term: term[0], dictionary)), 5, .80)

#Confirm the presence of an obscene word and returns tge true word
#@Param: a word and a sequence of closest matching words as a tuple
#@Return: list --> [the proper word if an obscenity is detected]
def confirmObscene(entity):
    word = entity[0]
    return [term for term in entity[1] \
            if round(difflib.SequenceMatcher(None, word.lower(), term).ratio(), 5) > .80000\
            or word.find(term) != -1] #Terms that have a direct match or are present in the word


#Performs the obscenity ranking
#@Param: text to be ranked in obscenity
#@Return: the ranking in obscenity of the text
punctuation = ['.', '!', '?', ',', '\'', '\\']
def rankText(text, slogans, amplifiers):
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

print sloganWeight('ass wipe black cock')