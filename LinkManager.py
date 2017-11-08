import csv
from HTMLParser import HTMLParser

import requests
from bs4 import BeautifulSoup


def store_book_links_to_csv(url, pages, file_name):
    i = 1
    while i < pages:
        print "Page " + str(i)
        i += 1
        r = requests.get(url + str(i) + ".html")
        soup = BeautifulSoup(r.content, "html.parser")
        reading_area = soup.find_all("div", attrs={'class': 'dirwraps'})
        htmlparser = HTMLParser()

        with open(file_name, 'ab', ) as f:
            writer = csv.writer(f)
            for link in soup.findAll('a', href=True):
                if 'books' in link['href']:
                    try:
                        bk_name = htmlparser.unescape(link.text)
                        bk_link = htmlparser.unescape(link['href'])
                        if "Next" in bk_name:
                            raise EOFError
                        if "Home" in bk_name:
                            raise EOFError
                        if "Previous" in bk_name:
                            raise EOFError
                        if "Last" in bk_name:
                            raise EOFError

                        print bk_name + " " + bk_link
                        writer.writerow([bk_name, bk_link])
                    except (EOFError, UnicodeEncodeError, UnicodeDecodeError) as e:
                        print(e)


def downloader(file_name):
    with open(file_name, 'rb') as csv_f:
        reader = csv.reader(csv_f, delimiter=',')
        for row in reader:
            bk_name = row[0]
            bk_link = row[1]
            print bk_name + " " + bk_link


# store_book_links_to_csv("http://www.readromancebook.com/books/", 78, "Books_Links.csv")
downloader("Books_Links.csv")
