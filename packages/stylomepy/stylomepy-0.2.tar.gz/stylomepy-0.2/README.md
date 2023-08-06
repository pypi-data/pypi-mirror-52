# Stylomepy

*Stylomepy* is a **Python** library for measuring the style of a text. It is available in Spanish and Engish languages.
It can be used in the analysis of the **statistics** of a text, the **readability index** of it, the **vocabulary richness**, **formality** and **coherence**.


# Installation

*Stylomepy* can be installed using *pip* and *Python 3.0* is needed:
```
pip3 install stylomepy
```

# Use of the library

When we have the text we want to analyze, it is necessary to create a *StyleMetrics* object that will include the style features of that text:
```python
import stylomepy
style = stylomepy.StyleMetrics(text, lang, MATTR_Window, MTLD_Limit, coherence, path)
```
Where *text* is the text to analyze, *lang* is the language of that text ('es', 'en'), *MATTR_Window* is the window size of the **MATTR algorithm** (usually **500** or **100**), *MTLD_Limit* is the limit of the **MTLD algorithm** (usually **0.72**), the field *coherence* is a **boolean** for analyze or not the **coherence** of the text and *path* is the path of the **Word Embeddings** model needed for measuring the **coherence** of the text.


## TextStatistics

To analyze the statistics of the text:
```python
style.getTextStatistics(index='index')
```
The available indexes are *sentencesCount*, *charPerSent*, *charPerWord*, *wordsPerSent*, *diffWords*, *conjunctions*, *adjectives*, *verbs*,  *nouns*, *adverbs*, *prepositions*, *determiners*, *pronouns*, *interjections*, *shortWords*, *commonWords*, *uncommonWords*.

## Readability Index

To analyze the readability difficulty of a text:
```python
style.getReadabilityIndex(index='index')
```
The available spanish indexes are *INFLESZ* and *Mu*. The available english indexes are *ARI*, *FleschRI* and *FogCount*.

## Vocabulary Richness

To analyze the lexical diversity of a text:
```python
style.getVocabularyRichness(index='index')
```
The available indexes are *TTR*, *MSTTR*, *MATTR*, *MTLD* and *HDD*.

## Formality

To analyze the formality score of a text:
```python
style.getFormalityIndex()
```
To analyze the adjective score of a text:
```python
style.getAdjScore()
```

## Coherence
To analyze the coherence of a text, when the *StyleMetrics* object is created, *coherence* attribute needs to be ***True*** and the path of the **Word Embeddings** model is needed too.
```python
style = stylomepy.StyleMetrics(text, 'es', 100, 0.72, True, 'word_embeddings_path')
style.getCoherenceIndex()
```
For Spanish texts, the model has to be a .txt format; for English texts, the model has to be a .bin format.

## Another way of use
If you want to use the library analyzing a few statistics, you do not need to create a *StyleMetrics* object. You can use some of the developed functions separately. The next examples show this:
```python
import stylomepy

adverbs = stylomepy.TextStatistics.wordClass(text, 'en')[4]
shortWords = stylomepy.TextStatistics.shortWords(text,'es')
lexDiversity = stylomepy.VocabularyRichness.MATTR(text, 100, 'es')
coherence = stylomepy.coherenceMetrics.coherenceMeasure(text, 'en', 'word_embeddings_path')
```

## Possible issues
When the library analyzes a Spanish text, an error could appear saying something like *NLTK was unable to find the java file!
Use software specific configuration paramaters or set the JAVAHOME environment variable.*. If it happens, run the next script and then use the library.
```python
import os
import nltk

java_path = "jdk_path"
os.environ['JAVAHOME'] = java_path

nltk.internals.config_java('jdk_path')

```
Where *jdk_path* is the **Java JDK** path in your system.

