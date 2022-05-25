text = """
In the third paragraph, the author describes the development of a brown coloring among certain mature caterpillars, which aids their survival in the daytime, when they hide among the sticks and twigs below their foods sources. It is clear that the author is arguing that the caterpillar’s coloring (“genetic adaptation”) follows and aids its habit of eating by night and hiding during the day (“behavioral patterns”) from the excerpt that reads, “We may then conclude that the habit of concealing themselves by day came first, and that the brown color is a later adaptation.”
"""

from tracemalloc import stop
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_sm')

doc = nlp(text)

tokens = [token.text for token in doc]
# print(tokens)

punctuation = punctuation + '\n'
# print(punctuation)

word_frequencies = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

# print(word_frequencies)

max_frequency = max(word_frequencies.values())

# print(max_frequency)

for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word]/max_frequency

# print(word_frequencies)

sentence_tokens = [sent for sent in doc.sents]
# print(sentence_tokens)


sentence_scores = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequencies.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_frequencies[word.text.lower()]
            else:
                sentence_scores[sent] += word_frequencies[word.text.lower()]
# print(sentence_scores)

from heapq import nlargest

select_length = int(len(sentence_tokens)*0.3)
# print(select_length)

summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
# print(summary)

final_summary = [word.text for word in summary]

summary = ' '.join(final_summary)
# print(summary)

# print(len(text))
# print(len(summary))