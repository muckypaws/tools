#!/usr/bin/python

import sys
import re
import string
import urllib3

# Initialise Dictionary
d={}
uniq_emails=d.keys()

# Strip Tags from Text
def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

# Search for Email within Search Engine Pages.
def searchForEmailFromWebPage(webPage):
    page_counter = 0
    try:
        httpReq = urllib3.PoolManager(num_pools=2, headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)"})

        while page_counter < max_pages_to_search :
            results = webPage + repr(page_counter) + '&sa=N'
            request = httpReq.request("GET",results)
            if int(request.status) >= 200 and int(request.status) < 300:
                emails = (re.findall('([\w\.\-]+@'+domain_name+')',StripTags(request.data.decode('utf-8'))))
                for email in emails:
                    d[email]=1
                    uniq_emails=d.keys()
                page_counter = page_counter +10
            else:
                page_counter = 9999999
                print("\nReturned Status: " + str(request.status))
    except IOError:
        print ("Cannot connect to Google Groups."+"")

#
# Start, Check we have domain name set
#
if len(sys.argv) < 2:
        print ("\nExtracts emails from Google results.\n")
        print ("\nUsage: ./goog-mail.py <domain> <optional_pages to search: default 50>\n")
        sys.exit(1)

# Get Command Line Parameters
domain_name=sys.argv[1]
max_pages_to_search = 50

#
# Check if requesting search over default pages
#
if len(sys.argv) == 3:
    max_pages_to_search = int(sys.argv[2])

print("Searching for domain:" + str(domain_name) + "  within: " + str(max_pages_to_search) + " Pages")
print("\nSearching: Google Groups\n")
webSearch = 'https://groups.google.com/groups?q='+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start='
searchForEmailFromWebPage(webSearch)

print("Searching: Google\n")
webSearch = 'http://www.google.com/search?q=%40'+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start=' 
searchForEmailFromWebPage(webSearch)

print("Searching: Bing\n")
webSearch = 'http://www.bing.com/search?q=%40'+str(domain_name)+'&hl=en&lr=&ie=UTF-8&first=' 
searchForEmailFromWebPage(webSearch)

for uniq_emails_web in d.keys():
    print (uniq_emails_web+"")
