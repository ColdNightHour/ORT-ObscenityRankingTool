# -*- coding: utf-8 -*-

#A library used to detect obscenity, though in a very minimal and primative manner
import difflib
import re
import time
import math
import collections

#Loads the obscenity dictionary from the directory
obscenities = ''
slogans = ''
amplifiers = ''

def splitter(term):
    final = term.split(',')
    return (final[0], (float(final[1]), final[2]))

def loadDictionaries():
    content = ''

    with open('./Dictionaries/obscenities.txt') as d:
        content = d.readlines()
    content = [ x.strip() for x in content ]
    obscenities = list(map(splitter, content))

    with open('./Dictionaries/slogans.txt') as d:
        content = d.readlines()
    obscenities = [ x.strip() for x in content ]

    

loadDictionary()

#Gets the close matches of a word
#@Param: word to be analyzed
#@Return: a sequence of obscene words that re best matches
def closeMatches(word):
    return difflib.get_close_matches(word, list(map(lambda term: term[0], dictionary)), 5, .80)

#Confirm the presence of an obscene word and returns tge true word
#@Param: a word and a sequence of closest matching words as a tuple
#@Return: the proper word if an obscenity is detected
def confirmObscene(entity):
    word = entity[0]
    return [term for term in entity[1] \
            if round(difflib.SequenceMatcher(None, word.lower(), term).ratio(), 5) > .80000\
            or word.find(term) != -1] #Terms that have a direct match or are present in the word

#def summation(list):

#Performs the obscenity ranking
#@Param: text to be ranked in obscenity
#@Return: the ranking in obscenity of the text
punctuation = ['.', '!', '?', ',', '\'', '\\']
def rankText(text):
    tokens = re.sub('[^A-Za-z ]+', '', text).split(' ')
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
    print (text  + "_______" + str(refinedMatches))
    print weight
    print frequencySum
    #rank = (math.log((weight*frequencySum), 2)*(len(refinedMatches))*(len(tokens) - len(refinedMatches) + 1))
    #return rank

#t0 = time.time()
print(rankText('dick ass fuck'))
print(rankText('I\'m so fucking mad right now. I need help'))
print(rankText('fuck the broncos, they can suck a dick'))
print(rankText('Fuck trump man, nigga is gay af'))
print(rankText('Did you cum in me!? Fuck you did huh you know what FUCK YOU fuck you fuck you, you fucking asshole.'))
