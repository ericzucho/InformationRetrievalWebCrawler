import robotparser

import operator

import math

from scorer import Scorer

def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]

max_to_display = 6

def print_query_result(all_words, word_matrix, normalized_matrix, stop_words,title_vocabulary_dict):
    doc_list = scorer.score_query(all_words, word_matrix, normalized_matrix, stop_words,title_vocabulary_dict)
    amount_displayed = 0
    for doc, score in sorted(doc_list.items(), key=operator.itemgetter(1), reverse=True):
        url, object = w.get_url_object_by_id(doc)
        amount_displayed += 1
        print "{0}. {1}".format(amount_displayed, object.title)
        print object.summary
        print "{0}.".format(url)
        print "Score: {0}\n".format(score)
        if amount_displayed == max_to_display:
            break
    return amount_displayed


if __name__ == "__main__":

    source = 'http://code.activestate.com/recipes/578060-a-simple-webcrawler/'

    from crawler import WebCrawler
    from dict_encoder import DictEncoder
    from matrix_builder import MatrixBuilder
    from stop_words import get_stop_words
    import re
    fmoore_url_regex = re.compile('https?\:\/\/lyle\.smu\.edu\/\~fmoore.*(htm|txt|html|php|\/)$')

    w = WebCrawler(fmoore_url_regex)

    stop_words = get_stop_words('en')

    w.start_crawling(['https://lyle.smu.edu/~fmoore/'],50,stop_words)

    print("------------------")
    print("CRAWLING FINISHED")
    print("------------------")

    for key,value in w.my_url_dict.items():
        print("URL: {0}, Title: {1}, Type: {2}".format(key, value.title, value.status))
    print "There is(are) {} graphic file(s).".format(w.image_links)
    print("------------------")
    print "Most common words:"
    for word in sorted(w.vocabulary_dict, key=lambda word: len(w.vocabulary_dict[word]), reverse=True)[:20]:
        print ("{0} ({1} times)".format(word,len(w.vocabulary_dict[word])))

    #encoder = DictEncoder()
    #encoded_dict = encoder.endoce_dict(w.vocabulary_dict,w.title_vocabulary_dict)
    #print encoded_dict

    scorer = Scorer()
    matrix_builder = MatrixBuilder()
    word_matrix,df_square_sums = matrix_builder.build(w.vocabulary_dict)
    normalized_matrix = matrix_builder.normalize(word_matrix,df_square_sums)

    q = open('queries.txt', 'r')
    t = open('thesaurus.txt', 'r')
    thesaurus_dict = {}
    for word in t:
        thesaurus_list = word.split()
        if len(thesaurus_list) < 2:
            continue
        thesaurus_dict[thesaurus_list[0]] = []
        for option in thesaurus_list[1:]:
            thesaurus_dict[thesaurus_list[0]].append(option)

    for query in q:
        all_words = query.replace("/"," ").split()
        if len(all_words) == 1 and all_words[0] == "stop":
            exit(0)
        print "\nQUERY: {0}".format(query.strip())
        amount_displayed = print_query_result(all_words, word_matrix, normalized_matrix, stop_words, w.title_vocabulary_dict)
        if amount_displayed < math.ceil(max_to_display/2):
            all_words = [thesaurus_dict[x] if x in thesaurus_dict else x for x in all_words]
            flat_all_words = flatten(all_words)
            if flat_all_words != all_words:
                print "Thesaurus expansion result"
                print_query_result(flat_all_words, word_matrix, normalized_matrix, stop_words,w.title_vocabulary_dict)

