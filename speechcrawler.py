# CS122: Course Search Engine Part 1
# THE CRAWLER -- Python file contains functions for crawling through the now defunct UChicago course catalog
# and collecting class titles, departments, course numbers, descriptions, professors, etc.
# and generating csv file that can easily later be inputted into a mysql database.
# Joseph Day -- Rogers Section -- PA 2

import re
import util
import bs4
import queue
import json
import sys
import csv
import requests
import pandas as pd
import pickle

INDEX_IGNORE = set(['a',  'also',  'an',  'and',  'are', 'as',  'at',  'be',
                    'but',  'by',  'course',  'for',  'from',  'how', 'i',
                    'ii',  'iii',  'in',  'include',  'is',  'not',  'of',
                    'on',  'or',  's',  'sequence',  'so',  'social',  'students',
                    'such',  'that',  'the',  'their',  'this',  'through',  'to',
                    'topics',  'units', 'we', 'were', 'which', 'will', 'with', 'yet'])

#starting_url = "https://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/index.html"
#limiting_domain = "classes.cs.uchicago.edu"

starting_url = "http://millercenter.org/president/speeches"
limiting_domain = "millercenter.org"
#starting_url = "https://www2.cbia.com/ieb/default.htm"

queue = queue.Queue(maxsize=0)
visited = []

def queue_children_sites(starting_url, queue):
    '''Given a url and a queue, adds all children urls
     of the start point to the queue
     Inputs: starting_url -- string that corresponds to a url
     queue -- queue.Queue object
     Outputs: None, queue is modified
     in place to contain all child urls'''
    
    response = requests.get(starting_url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    URLs = soup.find_all("a", {"class":"transcript"})
    #print(URLs)
    URLs = [URL["href"] for URL in URLs if URL.has_attr("href")]
    children = []
    for URL in URLs:
        if util.is_absolute_url(URL):
            children.append(URL)
        else:
            URL = util.convert_if_relative_url(starting_url, URL)
            children.append(URL)  

    children = [child for child in children if util.is_url_ok_to_follow(child, limiting_domain)]
    for child in children:
        queue.put(child)
            
def get_transcript(speech_link):
    ''' scrape title of speech, date of speech and full transcipt contained in the input speech_link URL '''
    
    #new_link = base_url + str(speech_link)
    try:
        response = requests.get(speech_link)
        soup = bs4.BeautifulSoup(response.content, "html5lib")
        title = soup.find("title").text
        speech_date = title.split('(', 1)[1].split(')')[0]
        transcript = soup.find('div', {'id': 'transcript'}).text
        transcript = transcript.replace('\n', ' ').replace('\r', '').replace('\t', '').replace('\'', '')
        speaking = speech_link.split('/')[4].capitalize()
        return {'speaker': speaking,
                'date': speech_date,
                'title': title,
                'transcript': transcript}
    except:
        pass



def crawl(queue=None):
    if queue is None:
        queue_children_sites(starting_url, queue)
    transcript_dict = {}
    i=0
    size = queue.qsize()
    while queue.qsize() > 0:
        if i % 100 == 0:
            print ('Scraped ' + str(i) + '/' + str(size) + ' of links...')
        link = queue.get()
        transcript_data = get_transcript(link)
        if transcript_data is not None:
            key = transcript_data['speaker'] + '|' + transcript_data['date']
            transcript_dict[key] = transcript_data
        i+=1
        print("queue size is " +  str(queue.qsize()))
        print("dict size is " + str(len(transcript_dict)))

    df = pd.DataFrame.from_dict(transcript_dict, orient='index')
    pickle.dump(df, open( "presidential_speeches2.pickle", "wb" ))