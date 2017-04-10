import robotparser


if __name__ == "__main__":

    source = 'http://code.activestate.com/recipes/578060-a-simple-webcrawler/'

    from crawler import WebCrawler
    from dict_encoder import DictEncoder
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

    encoder = DictEncoder()
    encoded_dict = encoder.endoce_dict(w.vocabulary_dict,w.title_vocabulary_dict)
    print encoded_dict