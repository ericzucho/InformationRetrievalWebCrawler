Eric Zuchovicki - 47125849
SMU - Information Retrieval and Web Search.

Initial source extracted from: http://code.activestate.com/recipes/578060-a-simple-webcrawler/
Porter stemmer extracted from: https://tartarus.org/martin/PorterStemmer/python.txt
Modifications were made to both.

Used software:
-> IDE: PyCharm.
-> Programming language: Python 2.7
-> Libraries: BeautifulSoup, robotparser, hashlib, httplib, socket, urllib, stop_words, re.

Installation:
-> Uncompress tar file.
-> Activate virtual environment. On Linux machine (Ubuntu):
   source eric_crawler_virtualenv/bin/activate

Usage:
-> Program takes 3 inputs, all hardcoded into the project.py file.
   -> A list of URLs where the crawler should start crawling.
      This is set only to 'https://lyle.smu.edu/~fmoore/'
   -> An integer that specifies the maximum amount of documents that should be crawled.
      This is set to 100
   -> A list of stop words that should be ignored.
      The stop words currently set are the ones returned by the method get_stop_words in the stop_words library, but can
      be replaced with any list of strings. The list of stop words can be seen here:
      https://github.com/Alir3z4/stop-words/blob/0e438af98a88812ccc245cf31f93644709e70370/english.txt
  Any of these input parameters can be changed directly by editing the project.py file, on line 17.
-> Program is run with
   python project.py
-> Output can be read directly from standard output.