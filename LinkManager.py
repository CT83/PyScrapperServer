import csv
from HTMLParser import HTMLParser

import requests
from bs4 import BeautifulSoup

url = "http://www.readromancebook.com/books/"
i = 1
while i < 100:
    print "Page " + str(i)
    i += 1
    r = requests.get(url + str(i) + ".html")
    soup = BeautifulSoup(r.content, "html.parser")
    reading_area = soup.find_all("div", attrs={'class': 'dirwraps'})
    htmlparser = HTMLParser()

    with open('Links.csv', 'a') as f:
        writer = csv.writer(f)
        for link in soup.findAll('a', href=True):
            if 'books' in link['href']:
                try:
                    bk_name = htmlparser.unescape(link.text)
                    bk_link = htmlparser.unescape(link['href'])
                    if "Next" in bk_name:
                        raise Exception
                    if "Home" in bk_name:
                        raise Exception
                    if "Previous" in bk_name:
                        raise Exception
                    if "Last" in bk_name:
                        raise Exception

                    print bk_name + " " + bk_link
                    writer.writerow([bk_name, bk_link])
                except Exception:
                    print "Exception"
