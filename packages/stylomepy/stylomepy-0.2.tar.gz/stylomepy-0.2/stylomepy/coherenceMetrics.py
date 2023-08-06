from gensim.models.keyedvectors import KeyedVectors
from gsitk.features.word2vec import Word2VecFeatures
import numpy
from . import TextStatistics as stats



def coherenceMeasure(text, lang, path):
    """Returns the cocherence of a text.
    
    This function measures the coherence of a text.
    First, a Word Embeddings model is loaded. Then, the text is tokenized in sentences.
    The sentences are tokenized too. Finally, the cosine similarity of the sentences
    is measured and the final result is the average of these measures.

    The available Word Embeddings formats are .bin for English texts and .txt for Spanish texts.
    
    """

    if lang == "en":
        w2v_extractor = Word2VecFeatures(w2v_model_path=path, w2v_format='google_bin', convolution=[1,0,0])
    elif lang == "es":
         w2v_extractor = Word2VecFeatures(w2v_model_path=path, w2v_format='google_txt', convolution=[1,0,0])

    sentences = stats.sentencesCount(text, lang)

    sentList = []

    for sent in range(sentences[0]):
        sentList.append(stats.tokenizar(sentences[1][sent], lang))

    transOpt = w2v_extractor.transform(sentList)

    transOpt[~numpy.isnan(transOpt).any(axis=1)]
    transOpt = transOpt[~numpy.all(transOpt == 0, axis=1)]

    sum = 0
    for sent in range(len(transOpt)-1):
        sims = w2v_extractor.model.cosine_similarities(transOpt[sent], transOpt)
        sum += sims[sent + 1]

    return sum/(len(transOpt) - 1) * 100