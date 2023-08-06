from . import TextStatistics as stats
from . import RIAlgorithms as ri
from . import VocabularyRichness as vr
from . import formality as form
from . import coherenceMetrics as coh

class StyleMetrics():

	def _setReadabilityIndex(self, text, lang):


		if lang == "en":
			readabilityIndexes = {'ARI': ri.ARI(text, lang), 
							'FleschRI': ri.fleschRI(text, lang),
							'FogCount': ri.fogCount(text, lang)
							}
		else:
			readabilityIndexes = {'INFLESZ': ri.INFLESZ(text, lang),
							'Mu': ri.muReadability(text, lang)
							}

		return readabilityIndexes

	def _setTextStatistics(self, text, lang):

		diffWords = stats.differentWords(text, lang)
		commonUncommonWords = stats.commonUncommonWords2(text, lang)
		wordsClasses = stats.wordClass(text, lang)

		statistics = {'sentencesCount': stats.sentencesCount(text, lang)[0],
							'charPerSent': stats.charactersPerSentence(text, lang),
							'charPerWord': stats.charactersPerWord(text, lang),
							'wordsPerSent': stats.wordsPerSentence(text, lang),
							'diffWords': diffWords[0],
							'conjunctions': wordsClasses[0],
							'adjectives': wordsClasses[1],
							'verbs': wordsClasses[2],
							'nouns': wordsClasses[3],
							'adverbs': wordsClasses[4],
							'prepositions': wordsClasses[5],
							'determiners': wordsClasses[6],
							'pronouns': wordsClasses[7],
							'interjections': wordsClasses[8],
							'shortWords': stats.shortWords(text, lang),
							'commonWords': commonUncommonWords[0],
							'uncommonWords': commonUncommonWords[1],
							}

		return statistics

	def __init__(self, text, lang, window, limit, coherence, path):
		if coherence:
			self._cIndex = coh.coherenceMeasure(text, lang, path)
		else:
			self._cIndex = 0
		self._fIndex = form.wfFormIndex(text, lang)
		self._adjScore = form.adfScore(text, lang)
		self._vIndex = {'TTR': vr.TTR(text, lang),
		 				'Others': vr.vbRichFunction(text, lang),
		 				'MSTTR': vr.MSTTR(text, lang), 
		 				'MATTR': vr.MATTR(text, window, lang),
						'MTLD': vr.MTLD(text, limit, lang),
						'HDD': vr.HDD(text, lang)
						}
		self._rIndex = self._setReadabilityIndex(text, lang)
		self._textStats = self._setTextStatistics(text, lang)
		
		
		


	def getCoherenceIndex(self):
		return self._cIndex

	def getFormalityIndex(self):
		return self._fIndex

	def getAdjScore(self):
		return self._adjScore

	def getReadabilityIndex(self, index = ''):

		result = ''

		if index in self._rIndex:
			result = self._rIndex[index]
		elif index == '':
			result = self._rIndex
		else:
			result = 'ERROR: Bad Index'

		return result

	def getVocabularyIndex(self, index = ''):

		result = ''

		if index in self._vIndex:
			result = self._vIndex[index]
		elif index == '':
			result = self._vIndex
		else:
			result = 'ERROR: Bad Index'

		return result

	def getTextStatistics(self, index = ''):

		result = ''

		if index in self._textStats:
			result = self._textStats[index]
		elif index == '':
			result = self._textStats
		else:
			result = 'ERROR: Bad Index'

		return result
