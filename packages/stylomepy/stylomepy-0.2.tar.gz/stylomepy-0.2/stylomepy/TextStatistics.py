import nltk
nltk.download('punkt')
nltk.download("popular")
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import StanfordPOSTagger
from nltk import FreqDist
import wordfreq
import contractions


def tokenizar(text, lang):
    """Splits in words a text.
    
    This function removes undesirable characters and extends English contractions.
    Then it appends each word to a list.
    Returns that list of words.
    
    """
    
    procText = text
    
    chars1 = "`´"
    chars2 = "-–¿¡/\\|"
    
    for char in chars1:
        procText = procText.replace(char, "'")
   
    if lang == "en":
        procText = contractions.fix(procText)
    
    for char in chars2:
        procText = procText.replace(char, ' ')
        
    procText = procText.replace(" \'", " ")
    
    tokens = nltk.word_tokenize(procText)
    tokens = ([token for token in tokens
               if any(c.isalpha() for c in token)])
    
    tokensOpt = []
    for token in tokens:
        if token[0] == "'":
            token = token[1:len(token)]
            
        elif token[len(token)-1] == ".":
            token = token[0:len(token)-1]
        if token != 's':
            tokensOpt.append(token)
    return tokensOpt

def sentencesCount(text, lang):
    """Calculates the number of sentences in the text.
    
    It tokenizes the text in different sentences thanks to a pre-trained Punkt tokenizer
    for the English language and for the Spanish language.
    Then, it counts how many sentences there are.
    Returns the number of sentences and a list with the text sentences.
    
    """
    procText = text
    
    chars1 = "`´"
    chars2 = "-–¿¡/\\"
    chars3 = "\n"
    chars4 = '  '
    
    for char in chars1:
        procText = procText.replace(char, "'")
   
    if lang == "en":
        procText = contractions.fix(procText)
         #The NLTK data package includes a pre-trained Punkt tokenizer for English.
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        
    elif lang == "es":
        sent_detector = nltk.data.load('tokenizers/punkt/spanish.pickle')
        
    for char in chars2:
        procText = procText.replace(char, ' ')
        
    procText = procText.replace(chars3, ' ')
    procText = procText.replace(chars4, ' ')  
    
        
    sentences = sent_detector.tokenize(procText.strip())
    sentNumber = len(sentences)
    
    for sent in sentences:
        if sent.find('\n\n') != -1:
            sentNumber +=1

    return sentNumber, sentences

def charactersPerSentence(text, lang):
    """Calculates an average of the number of characters per sentence.
    
    The function returns an average of the number of characters per sentence.
    
    """
    sentencesNumber = sentencesCount(text,lang)[0]
    tokens = tokenizar(text, lang)

    charPerSent = 0
    
    for token in tokens:
        charPerSent += len(token)
        
    charPerSent /= sentencesNumber
    
    return charPerSent

def charactersPerWord(text, lang):
    """Calculates an average of the number of characters per word.
    
    The function returns an average of the number of characters per word.
    
    """
    tokens = tokenizar(text, lang)
    
    wordsNumber = len(tokens)
    
    charPerWord = 0
    
    for token in tokens:
        charPerWord += len(token)
        
    charPerWord /= wordsNumber
    
    return charPerWord


def differentWords(text, lang):
    """Identifies the different words within the text.
    
    Returns the number of different words and a list with them.
    The function replaces uppercase with lowercase.
    
    """
    
    diffWordsList = []
    tokens = tokenizar(text, lang)
    tokensLower = []
    for token in tokens:
        tokensLower.append(token.lower())
    tokensLower.sort()

    i = 0
    for token in tokensLower:
        if i+1 < len(tokensLower):
            if token != tokensLower[i + 1]:
                diffWordsList.append(token)
        else:
            diffWordsList.append(token)
        i += 1
    
    return len(diffWordsList), diffWordsList

def wordClass(text, lang):
    """It searchs the different types of words in the text
    
    It tokenizes the text in tagged words. Then, and thanks to the tags,
    it classifies the words by class and save the words in different lists.
    It returns the number of conjunctions, adjectives, verbs, nouns, adverbs, prepositions,
    determiners, pronouns and interjections..
    
    """

    tokens = tokenizar(text, lang)

    
    nouns = []
    verbs = []
    adjectives = []
    adverbs = []
    conjunctions = []
    prepositions = []
    determiners = []
    pronouns = []
    interjections =[]
    
    if lang == "en":
        
        taggedTokens = nltk.pos_tag(tokens)
        
        for tupla in taggedTokens:
            if tupla[1] == "CC":
                conjunctions.append(tupla[0])
            elif tupla[1][0] == "J":
                adjectives.append(tupla[0])
            elif tupla[1][0] == "V":
                verbs.append(tupla[0])
            elif tupla[1][0] == "N":
                nouns.append(tupla[0])
            elif tupla[1][0] == "R" or tupla[1] == "WRB":
                adverbs.append(tupla[0])
            elif tupla[1] == "TO" or tupla[1] == "IN":
                prepositions.append(tupla[0])
            elif tupla[1] == "WDT" or tupla[1] == "PDT" or tupla[1] == "DT":
                determiners.append(tupla[0])
            elif tupla[1] == "PRP" or tupla[1] == "PRP$" or tupla[1] == "WP" or tupla[1] == "WP$":
                pronouns.append(tupla[0])
            elif tupla[1] == "UH":
                interjections.append(tupla[0])
            
        result = [len(conjunctions), len(adjectives), len(verbs), len(nouns), len(adverbs), len(prepositions),
                  len(determiners), len(pronouns), len(interjections)]
            
            
    elif lang == "es":
        
        tagger = r"stylomepy/stanfordPosTagger/models/spanish.tagger"
        jar = r"stylomepy/stanfordPosTagger/stanford-postagger.jar"
        taggedTokens = StanfordPOSTagger(tagger,jar).tag(tokens)

        for tupla in taggedTokens:
            if tupla[1][0] == "c":
                conjunctions.append(tupla[0])
            elif tupla[1][0] == "a":
                adjectives.append(tupla[0])
            elif tupla[1][0] == "v":
                verbs.append(tupla[0])
            elif tupla[1][0] == "n":
                nouns.append(tupla[0])
            elif tupla[1][0] == "r":
                adverbs.append(tupla[0])
            elif tupla[1][0] == "s":
                prepositions.append(tupla[0])
            elif tupla[1][0] == "d":
                determiners.append(tupla[0])
            elif tupla[1][0] == "p":
                pronouns.append(tupla[0])
            elif tupla[1][0] == "i":
                interjections.append(tupla[0])
        
        result = [len(conjunctions), len(adjectives), len(verbs), len(nouns), len(adverbs), len(prepositions),
                  len(determiners), len(pronouns), len(interjections)]
    
    
    return result


def wordsPerSentence(text, lang):
    """Calculates an average of the words per sentence.
    
    Return the average of words per sentence.
    
    """    
    sentences = sentencesCount(text, lang)[1]
    
    tokens = tokenizar(text, lang)

    wordsPerSent = len(tokens)/len(sentences)
    
    return wordsPerSent

def shortWords(text, lang):
    """It counts the number of short words within the text.
    
    It returns the number of words with 3 characters or less (Short Words).
    
    """
    tokens = tokenizar(text, lang)

    shortWords = 0
    for token in tokens:
        if len(token) <= 3:
            shortWords += 1
            
    return shortWords

def commonUncommonWords1(text, lang):
    """It counts the common and uncommon words in the text.
    
    Based in the comparation of the words in text with an english dictionary.
    If the word exists in the dictionary, we add 1 to common words. If doesn't,
    we will add 1 to uncommon words.
    It returns the number of common and uncommon words.
    It is only value for English texts.
    
    """
    diffWords = differentWords(text, lang)
    wnLem = WordNetLemmatizer()
    tokensText = ([token.lower() for token in diffWords[1]
                    if any(c.isalpha() for c in token)])
    englishVocab = ([token.lower() for token in nltk.corpus.words.words()
                      if any(c.isalpha() for c in token)])
    
    commonWords = 0
    uncommonWords = 0
    #tags=['a','n','v','r']
    
    def find(token):
        for englishWord in englishVocab:
            if token == englishWord:
                return True
        return False

    for token in tokensText:
        
        if find(token):
            commonWords += 1
        elif find(wnLem.lemmatize(token, pos='a')):
            commonWords += 1
        elif find(wnLem.lemmatize(token, pos='n')):
            commonWords += 1
        elif find(wnLem.lemmatize(token, pos='v')):
            commonWords += 1
        elif find(wnLem.lemmatize(token, pos='r')):
            commonWords += 1
        else:
            uncommonWords += 1
             
    return commonWords, uncommonWords

#Zipf Law
def commonUncommonWords2(text, lang):
    """ Analyzes a text searching for common and uncommon words.
    
    It uses wordfreq library for searching common and uncommon words
    in English or Spanish languages.
    
    Returns the number of common and uncommon words.
    
    """
    diffWords = differentWords(text, lang)[1]
    
    commonWords = 0
    uncommonWords = 0
    
    for token in diffWords:
        if wordfreq.zipf_frequency(token, lang) > 2:
            commonWords += 1
        else:
            uncommonWords += 1
            
    return commonWords, uncommonWords

def freqWords(text, lang):
    """Calculates the frequency of each word within a text
    
    Returns de most common words.
    
    """
    tokens = tokenizar(text, lang)
    tokensLower = []
    for token in tokens:
        tokensLower.append(token.lower())
    fdist = FreqDist(tokensLower)
    return fdist.most_common()

def removeStopWords(text, lang):
    """Removes the stop words in English or Spanish languages
    
    """
    if lang == "en":
        stopWords = set(stopwords.words("english"))
    elif lang == "es":
        stopWords = set(stopwords.words("spanish"))
    words = tokenizar(text, lang)
    wordsFiltered = []

    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)
 
    return wordsFiltered, len(wordsFiltered)
