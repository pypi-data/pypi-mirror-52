from __future__ import unicode_literals
import nltk
from . import TextStatistics as stats
import math
from .Silabizator import englishSilabizer, spanishSilabizer

def ARI(text, lang):
    """Calculates the Automated Readability Index of an English text.
    
    The function returns the two available ARI's metrics of the library.
    The first is the clasical ARI and the second is the optimized ARI.
    
    """

    tokens = stats.tokenizar(text, lang)
    sentenceNumber = stats.sentencesCount(text,lang)[0]
    wordsNumber = len(tokens)
    
    charNumber = 0
    for token in tokens:
        charNumber += len(token)


    avgCharPerWord = charNumber/wordsNumber
    avgWordsPerSentence = wordsNumber/sentenceNumber


    oldReadIndex = math.ceil(4.71*(avgCharPerWord) + 0.5*(avgWordsPerSentence) - 21.43)

    newReadIndex = math.ceil(5.84*(avgCharPerWord) + 0.37*(avgWordsPerSentence) - 26.01)
            
    return oldReadIndex, newReadIndex


def fleschRI(text, lang):
    """Calculates the Flesch Readability Index of an English text.
    
    This function returns the two available Flesch's metrics of the library.
    The first is the Flesch Reading Ease Index and the second is the
    Flesch-Kincaid Grade Level Index.
    
    """
    
    tokens = stats.tokenizar(text, lang)
    sentenceNumber = stats.sentencesCount(text,lang)[0]
    wordsNumber = len(tokens)

    syllablesNumber = 0
    s = englishSilabizer()
    for token in tokens:
        syllablesNumber += s(token)    

    avgSyllPerWord = syllablesNumber/wordsNumber
    avgWordsPerSentence = wordsNumber/sentenceNumber

    fleschReadingEase = 206.835 - 1.015*(avgWordsPerSentence) - 84.6*(avgSyllPerWord)
    fleschKincaidGradeLevel = 0.39*(avgWordsPerSentence) + 11.8*(avgSyllPerWord) - 15.59
    
    return fleschReadingEase, fleschKincaidGradeLevel

def fogCount(text, lang):
    """Calculates the Fog Count Index of an English text.
    
    The function returns the two available Fog Count's metrics of the library.
    The first is the clasical Fog Count and the second is the optimized Fog Count.
    
    """

    tokens = stats.tokenizar(text, lang)
    sentenceNumber = stats.sentencesCount(text,lang)[0]
    wordsNumber = len(tokens)
    oldFogCount = 0
    newFogCount = 0

    easyWords = []
    hardWords = []
    s = englishSilabizer()
    for token in tokens:
        if s(token) > 2:
            hardWords.append(token)
        else:
            easyWords.append(token)


    avgFogCount = (len(easyWords) + 3 * len(hardWords))/sentenceNumber

    if avgFogCount >= 20:
        oldFogCount = avgFogCount/2
    else:
        oldFogCount = (avgFogCount - 2)/2
    
    newFogCount = (avgFogCount - 3)/2
                
    return oldFogCount, newFogCount

def INFLESZ(text, lang):
    """Calculates the INFLESZ Index of a Spanish text.
    
    The function returns the INFLESZ Readability Index value of a
    text written in Spanish.
    
    """

    tokens = stats.tokenizar(text, lang)
    sentenceNumber = stats.sentencesCount(text,lang)[0]
    wordsNumber = len(tokens)

    s = spanishSilabizer()
    syllablesNumber = 0
    for token in tokens:
        syllablesNumber += len(s(token))
    
    inflesz = 206.835 - ((62.3*syllablesNumber)/wordsNumber)-(wordsNumber/sentenceNumber)
    
    return inflesz

def muReadability(text, lang):
    """Calculates the mu Readability Index of a Spanish text.
    
    The function returns the mu Readbility Index of a text written
    in Spanish.
    
    """

    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    charsPerWord = stats.charactersPerWord(text, lang)
    
    variance = 0
    for token in tokens:
        variance += ((len(token)-charsPerWord)**2)
        
    variance /= wordsNumber
    
    mu = ((wordsNumber/(wordsNumber - 1)) * (charsPerWord/variance)) * 100
        
    return mu   