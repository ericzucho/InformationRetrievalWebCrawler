import string

import math

from porter import PorterStemmer


class Scorer():

    def score_query(self,query,word_matrix,normalized_matrix,stop_words_list):
        porter_stemmer = PorterStemmer()
        square_sum = 0
        words = {}

        for word in query:
            word_without_punctuation = word.strip(string.punctuation).replace(" ", "").lower()
            if word_without_punctuation not in stop_words_list:
                stemmed_word = porter_stemmer.stem(word_without_punctuation,0,len(word_without_punctuation)-1)
                if stemmed_word not in words:
                    words[stemmed_word] = {}
                    words[stemmed_word]['repetitions'] = 0
                words[stemmed_word]['repetitions'] += 1

        for word,elements in words.items():
            square_sum += math.pow(elements['repetitions'],2)
        for word,elements in words.items():
            if word in word_matrix:
                words[word]['normalized'] = words[word]['repetitions'] / math.sqrt(square_sum)
                words[word]['weight'] = words[word]['normalized'] * word_matrix[word]['idf']
            else:
                words[word]['normalized'] = 0
                words[word]['weight'] = 0
        aggregate_scores = {}
        for word,elements in words.items():
            if word in normalized_matrix:
                for doc_id,doc_weight in normalized_matrix[word].items():
                    if doc_id not in aggregate_scores:
                        aggregate_scores[doc_id] = 0
                    aggregate_scores[doc_id] += doc_weight * elements['weight']
        return aggregate_scores
