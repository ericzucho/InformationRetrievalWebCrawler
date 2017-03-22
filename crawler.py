import re
import string


class Tag:
    name = '';
    text = '';
    first_child = 0;
    parent = 0;
    next_sibling = 0;
    closed = 0;
    depth = 0;
    def get_tag_info_str(self):
        c,p,s = 'none','none','none'
        if self.first_child != 0:
            c = self.first_child.name
        if self.parent != 0:
            p = self.parent.name
        if self.next_sibling != 0:
            s = self.next_sibling.name
        return "name = {}, text = {}\nParent = {}, First Child = {}, Next Sibling = {}\nClosed = {}, Depth = {}\n".format(self.name, self.text, p, c, s, self.closed, self.depth)
      
      
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    tag_list = []
    depth = 0;
    previous_tag = 'none';
    mode = 'silent';
  
  
    def handle_starttag(self, tag, attrs):
        if self.mode != 'silent':
            print "Start tag:", tag
            for attr in attrs:
                print "     attr:", attr
        self.depth = self.depth + 1
        t = Tag()
        t.name = tag
        t.depth = self.depth
        if self.previous_tag == 'start':
            # current tag is a first child of the last tag
            t.parent = self.tag_list[len(self.tag_list)-1]
            self.tag_list[len(self.tag_list)-1].first_child = t
        elif self.previous_tag == 'end':
            # current tag is next sibling of the last tag
          
            for x in reversed(self.tag_list):
                if x.depth == self.depth:
                    x.next_sibling = t          
                    if t.parent == 0:
                        t.parent = x.parent
                    break
        elif self.previous_tag == 'startend':
            # current tag is the next sibling of the previous tag
            t.parent = self.tag_list[len(self.tag_list)-1].parent
            self.tag_list[len(self.tag_list)-1].next_sibling = t
          
      
        self.tag_list.append(t)  
        self.previous_tag = 'start'
    def handle_endtag(self, tag):
        if self.mode != 'silent':
            print "End tag  :", tag
        for x in reversed(self.tag_list):
            if x.name == tag and x.closed == 0:
                x.closed = 1
                break
        self.depth = self.depth - 1
        self.previous_tag = 'end'
      
    def handle_startendtag(self, tag, attrs):
        if self.mode != 'silent':
            print "Start/End tag  :", tag
            for attr in attrs:
                print "     attr:", attr
        t = Tag()
        self.depth = self.depth + 1
        t.name = tag
        t.depth = self.depth
        t.closed = 1
          
        if self.previous_tag == 'start':
            # current tag is first child of the last tag
            t.parent = self.tag_list[len(self.tag_list)-1]
            self.tag_list[len(self.tag_list)-1].first_child = t
        elif self.previous_tag == 'startend':          
            # current tag is next sibling of last tag
            t.parent = self.tag_list[len(self.tag_list)-1].parent
            self.tag_list[len(self.tag_list)-1].next_sibling = t
        elif self.previous_tag == 'end':          
            # current tag is next sibling of a previous tag of depth = self.depth
            for x in reversed(self.tag_list):
                if x.depth == self.depth:
                    x.next_sibling = t          
                    if t.parent == 0:
                        t.parent = x.parent
                    break
          
        self.tag_list.append(t)  
        self.depth = self.depth - 1
        self.previous_tag = 'startend'
      
      
    def handle_data(self, data):
        if self.mode != 'silent':
            print "Data     :", data
      
        self.depth = self.depth + 1
      
        # add data to last tag in list with depth = current depth - 1
        for x in reversed(self.tag_list):
            if x.depth == self.depth - 1:
                x.text = (x.text + ' ' + data.strip(' \n\t')).strip(' \n\t')
                break
              
        self.depth = self.depth - 1
      
    def handle_comment(self, data):
        if self.mode != 'silent':
            print "Comment  :", data
    def handle_entityref(self, name):
        if self.mode != 'silent':
            c = unichr(name2codepoint[name])
            print "Named ent:", c
    def handle_charref(self, name):
        if self.mode != 'silent':
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            print "Num ent  :", c
    def handle_decl(self, data):
        if self.mode != 'silent':
            print "Decl     :", data
      
    def print_tag_list(self, u):
        for l in self.tag_list:
            print l.get_tag_info_str()
          
    def clear_tag_list(self):
        self.tag_list.__delslice__(0,len(self.tag_list))
    
    def pretty_print_tags(self):
        for t in self.tag_list:
            s = ''
            s = s + self.get_indent_str(t.depth-1)
            s = s + self.get_tag_str(t.name)
            print s

    def get_indent_str(self, n):
        s = ''
        while(n != 0):
            s = s + '    '
            n = n - 1          
        return s
          
    def get_tag_str(self, name):
        return '<{}>'.format(name)
      
    def find_first_tag(self, name):
        r = 0
        for t in self.tag_list:
            if t.name == name:
                r = t
                break
        return r
      
    def print_first_tag_info(self, name):
        t = self.find_first_tag(name)
        if t == 0:
            print "Tag: {} not found".format(name)
        else:
            print t.get_tag_info_str()

import urllib
import socket
socket.setdefaulttimeout(10)
import httplib
import robotparser
import hashlib
from bs4 import BeautifulSoup
from porter import PorterStemmer

class UrlData(object):
    def __init__(self,doc_id_counter):
        self.status = "OtherDocumentFormat"
        self.title = "NONE"
        self.page_hash = ""
        self.doc_id = doc_id_counter

def normalize_link(link,current_page):
    new_link = link
    if re.match("\'.*\'", new_link):
        new_link = re.sub(r'\'(.*)\'', r'\1', new_link)
    if re.match("\".*\"", new_link):
        new_link = re.sub(r'\"(.*)\"', r'\1', new_link)
    if not re.match("http(s)?\:\/\/", new_link):
        new_link =  re.search("(.*\/)",current_page).group(0) + new_link
    if re.match("http\:\/\/", new_link):
        new_link = re.sub(r'(http)', r'\1s', new_link)
    if re.match(".*\.\.\/.*", new_link):
        new_link = re.sub(r'[^\/]*\/\.\.\/', '', new_link)
    return new_link

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def denormalize_link(url):
    return re.search("\~fmoore(.*)",url).group(1)


class WebCrawler:
    """A simple web crawler"""
      
    link_dict = {}
    amount_of_pages_remaining = 9999
    #filter_list = [];
    parser = 0
    re_compiled_obj = 0
    image_links = 0
    my_url_dict = {}
    vocabulary_dict = {}
    doc_id_counter = 0
    stop_words_list = []
    porter_stemmer = PorterStemmer()

    class PageInfo:
        """ i store info about a webpage here """
        has_been_scraped = 0
        word_dict = {}
                 
          
    def __init__(self,re_compiled_obj):      
        #self.filter_list.append(self.Filter(1,'.cnn.'))
        self.parser = MyHTMLParser()
        self.re_compiled_obj = re_compiled_obj
          
    def get_page(self,url):
        """ loads a webpage into a string """
        page = ''
        try:
            f = urllib.urlopen(url=url)
            page = f.read()
            f.close()
        except IOError:
            print "Error opening {}".format(url)
        except httplib.InvalidURL, e:
            print "{} caused an Invalid URL error.".format(url)
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code        
                
        return page
  
    def check_filters(self,url):
        """ If the url_str matches any of the
        enabled filter strings
        then put the url in the dictionary """
        
        img_pattern = re.compile(".*\.(jpg|jpeg|png|tif|gif)$", re.IGNORECASE)
        not_outgoing_pattern = re.compile("https?\:\/\/lyle\.smu\.edu\/\~fmoore.*$", re.IGNORECASE)
        crawleable_document_pattern = re.compile(".*(htm|txt|html|\/)$", re.IGNORECASE)
        if img_pattern.match(url):
            self.image_links += 1
        if url not in self.my_url_dict:
            self.my_url_dict[url] = UrlData(self.doc_id_counter)
            self.doc_id_counter+= 1
            if not not_outgoing_pattern.match(url):
                self.my_url_dict[url].status = "OutgoingLink"
            else:
                if img_pattern.match(url):
                    self.my_url_dict[url].status = "ImageLink"
                else:
                    if crawleable_document_pattern.match(url):
                        self.my_url_dict[url].status = "CrawleableDocument"

        match = self.re_compiled_obj.search(url)
        #print "match = {}".format(match)
        return match
  
      
    def find_h1_tag(self,s,pos):
        """ finds the first <h1> tag """
        start = s.find('<h1>',pos)
        end = s.find('</h1>',start)
        return start, end

    def save_tag_text(self, tag, d):
        """ stores each word in the tag in a dictionary """
        if tag != 0:
            token_list = tag.text.split(' ')
            for token in token_list:
                #print 'token = {}'.format(token)
                if d.has_key(token):
                    d[token] = d[token] + 1
                else:
                    d[token] = 1
        return d
      
    def save_page_text(self,page_str):
        """ Save all important text on the page """
        offset = 0
        d = {}
      
        while offset != -1:
            start,end = self.find_h1_tag(page_str,offset)
            offset = end
      
            if start != -1 and end != -1:
                h1_tag = page_str[start:end+5]
                #print h1_tag
                self.parser.clear_tag_list()
                # turn text into linked list of tags
                # only feed part of the page into the parser
                self.parser.feed(h1_tag)                                 
                #self.parser.pretty_print_tags()
                tag = self.parser.find_first_tag('h1')
                # add words from tag into the dictionary
                d = self.save_tag_text(tag,d)
        return d
      
    def save_all_links_on_page(self,page_str,url,limit=60):
        """ Stores all links found on the current page in a dictionary """
        d = {}
        offset = 0
        i = 0
        num_pages_filtered = 0
        num_duplicate_pages = 0
        while offset != -1:
            if i == limit:
                break
            offset = page_str.lower().find('<a href=',offset)
            if offset != -1:
                start = offset + 7
                end = page_str.find('>',start+1)
                link = page_str[start+1:end]
                # don't just save all the links
                # filter the links that match specified criteria
                link = normalize_link(link,url)
                if self.check_filters(link):
                    if link not in self.link_dict:
                        # adding link to global dictionary
                        self.link_dict[link] = self.PageInfo()
                        # adding link to local dictionary
                        d[link] = self.PageInfo()
                    else:
                        num_duplicate_pages = num_duplicate_pages + 1
                else:
                    num_pages_filtered = num_pages_filtered + 1
                offset = offset + 1
            i = i + 1
        print "{} out of {} links were filtered (non-crawleable)".format(num_pages_filtered,i)
        print "{} out of {} links refered to URLs already seen".format(num_duplicate_pages,i)
        #print "{} links are being returned from save_all_links".format(len(d))
        return d
  
    def get_page_title(self,page_str):
        start = page_str.find('<TITLE>', 0)
        if start == -1:
            start = page_str.find('<title>', 0)
        end = page_str.find('</TITLE>',start+1)
        if end == -1:
            end = page_str.find('</title>',start+1)
        if start != -1 and end != -1:
            title =  page_str[start+7:end]
        else:
            title = "NOT FOUND!"
        return title

    def save_all_links_recursive(self,links,robots_parser):
        """ Recursive function that
            1) converts each page (link) into a string
            2) stores all links found in a dictionary """
        d = {}
      
        print "We can still crawl {} pages".format(self.amount_of_pages_remaining)
      
        if self.amount_of_pages_remaining > 0:
            self.amount_of_pages_remaining = self.amount_of_pages_remaining - 1
            urls = links.viewkeys()
            #print "There are {} urls".format(len(urls))
            for url in urls:
                if not (robots_parser.can_fetch("*", url) and robots_parser.can_fetch("*", denormalize_link(url))):
                    print "access to {} is forbidden by the robots.txt".format(url)
                    if url in self.my_url_dict:
                        self.my_url_dict[url].status = "ForbiddenRobots"
                    continue
                print "trying to get {} over the internet".format(url)
                page_str = self.get_page(url)
                print "done getting {} over the internet.".format(url)
                page_title = self.get_page_title(page_str)
                page_hash = hashlib.md5(page_str.encode('utf-8')).hexdigest()
                duplicate_found = False
                for single_url,url_info in self.my_url_dict.items():
                    if url_info.page_hash == page_hash:
                        duplicate_found = True
                        print "Document is an exact duplicate of {}".format(single_url)
                        break
                if duplicate_found:
                    self.my_url_dict[url].status = "Duplicate"
                else:
                    self.my_url_dict[url].page_hash = page_hash
                if page_title == "404 Not Found":
                    self.my_url_dict[url].status = "BrokenLink"
                else:
                    self.my_url_dict[url].title = page_title
                print "TITLE: {}".format(page_title)
                self.link_dict[url].word_dict = self.save_page_text(page_str)
                d = self.save_all_links_on_page(page_str,url)
                self.link_dict[url].has_been_scraped = 1

                self.count_words(page_str,url)


                # d contains all the links found on the current page
                self.save_all_links_recursive(d,robots_parser)

    def start_crawling(self,seed_pages,amount_of_pages,stop_words_list = []):
        """ User calls this function to start crawling the web """
        d = {}
        self.link_dict.clear()
       
        # initialize global dictionary variable to the seed page url's passed in
        for page in seed_pages:           
            self.link_dict[page] = self.PageInfo()
            d[page] = self.PageInfo()
            self.my_url_dict[page] = UrlData(self.doc_id_counter)
            self.doc_id_counter += 1
        self.amount_of_pages_remaining = amount_of_pages
        self.stop_words_list = stop_words_list
        rp = robotparser.RobotFileParser()
        rp.set_url("https://lyle.smu.edu/~fmoore/robots.txt")
        rp.read()
        # start a recursive crawl
        # can't pass in self.link_dict because then i get a RuntimeError: dictionary changed size during iteration
        self.save_all_links_recursive(d,rp)

    def print_all_page_text(self):
        """ prints contents of all the word dictionaries """
        for i in range(len(self.link_dict)):
            page_info = self.link_dict.values()[i]
            url = self.link_dict.keys()[i]
            print 'url = {}, has_been_scraped = {}'.format(url,page_info.has_been_scraped)
            d = page_info.word_dict
            for j in range(len(d)):
                word = d.keys()[j]
                count = d.values()[j]
                print '{} was found {} times'.format(word,count)

    def count_words(self,page_str,url):
        soup = BeautifulSoup(page_str, "lxml")
        data = soup.findAll(text=True)
        all_text = filter(visible, data)
        doc_id = self.my_url_dict[url].doc_id
        for line in all_text:
            for word in line.replace("/"," ").split():
                word_without_punctuation = word.strip(string.punctuation).replace(" ", "").lower()
                if word_without_punctuation not in self.stop_words_list:
                    stemmed_word = self.porter_stemmer.stem(word_without_punctuation,0,len(word_without_punctuation)-1)
                    if stemmed_word != "":
                        if stemmed_word not in self.vocabulary_dict:
                            self.vocabulary_dict[stemmed_word] = []
                        self.vocabulary_dict[stemmed_word].append(doc_id)
