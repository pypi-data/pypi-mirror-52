from . import TextStatistics as stats
import math
from scipy.stats import hypergeom



def TTR(text, lang):
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    diffWords = stats.differentWords(text, lang)[0]
    #TTR Type/Token ratio
    TTR = (diffWords/wordsNumber)
    return TTR

def vbRichFunction(text, lang):
    
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    diffWords = stats.differentWords(text, lang)[0]

    #Guiraud index
    guiraud = (diffWords/math.sqrt(wordsNumber))
    #Index Herdan
    herdan = (math.log10(diffWords)/math.log10(wordsNumber))
    #Index Uber
    uber = (math.pow((math.log10(wordsNumber)),2)/(math.log10(wordsNumber)-math.log10(diffWords)))
    #Mass
    mass = (math.log10(wordsNumber) - math.log10(diffWords))/(math.pow(math.log10(wordsNumber),2))
    
    
    return guiraud, herdan, uber, mass


def MSTTR(text, lang):
    
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    if wordsNumber < 100:
        return "The text length is too short to apply MSTTR"
    MSTTR = 0
    i = 0
    auxList = []
    segmentsNumber = 0
    for token in tokens:
        if len(auxList) < 100:
            auxList.append(token)              
            i += 1
        else:
            MSTTR += TTR(' '.join(auxList), lang)
            auxList = []
            segmentsNumber += 1
            if wordsNumber - i >= 100:
                continue
            else:
                break
    for token in reversed(tokens):
    	if len(auxList) < wordsNumber - i:
    		auxList.append(token)
    	else:
    		break
    MSTTR += TTR(' '.join(auxList), lang)
    segmentsNumber += 1
                
    return MSTTR/segmentsNumber * 100, segmentsNumber

def MATTR(text, window, lang):
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    if window > wordsNumber:
        return "The text is too short to apply this window"
    MATTR = 0
    auxList = []
    j = 0
    while j + window <= wordsNumber:
        for i in range(j, window + j):
            auxList.append(tokens[i])
        j += 1
        MATTR += TTR(' '.join(auxList), lang)
        auxList = []
    return MATTR/(j) *100

def MTLD(text, limit, lang):
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    def MTLDimplementation(usedTokens, limit):
        nSegm = 0
        segment = []

        for i in range(0, wordsNumber):
            segment.append(usedTokens[i])
            if TTR(' '.join(segment), lang) < limit:
                nSegm += 1
                segment = []
            elif i == wordsNumber - 1 and TTR(' '.join(segment), lang) > limit:
                rest = 1 - TTR(' '.join(segment), lang)
                nSegm += rest/(1 - limit)
        return wordsNumber/nSegm
    
    MTLD1 = MTLDimplementation(tokens, limit)
    MTLD2 = MTLDimplementation(tokens[::-1], limit)
    
    result = (MTLD1 + MTLD2)/2

    if result > 100:
        return 100
    else:
        return result

def HDD(text, lang):
    tokens = stats.tokenizar(text, lang)
    wordsNumber = len(tokens)
    freqWords = stats.freqWords(text, lang)
    probSum = 0
    k = 1
    lista = []
    for i in range(0, len(freqWords)):
        [N, d, n] = [wordsNumber, freqWords[i][1], 42]
        probType = hypergeom.pmf(k, N, d, n)
        probSum += probType
        lista.append(probType)  
        
    return probSum/42 *100