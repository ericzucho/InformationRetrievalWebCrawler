import robotparser


if __name__ == "__main__":

    source = 'http://code.activestate.com/recipes/578060-a-simple-webcrawler/'

    from crawler import WebCrawler
    import re
    fmoore_url_regex = re.compile('https\:\/\/lyle\.smu\.edu\/\~fmoore.*(htm|txt|html|\/)$')

    w = WebCrawler(fmoore_url_regex)
    w.start_crawling(['https://lyle.smu.edu/~fmoore/'],100)
    print "There is(are) {} graphic file(s).".format(w.image_links)