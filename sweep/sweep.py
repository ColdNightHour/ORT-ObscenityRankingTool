#TO BE USED FOR SCOURING and adding new terms

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
