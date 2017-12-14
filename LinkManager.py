import csv
import string
import time
import unicodedata
from HTMLParser import HTMLParser

import requests
from bs4 import BeautifulSoup

from FileManagement import write_convert_and_rename
from Scrapper import url_generator, scrape_book

website = 'readromancebook.com'


def store_book_links_to_csv(url, pages, file_name):
    i = 1
    while i < pages:
        print "Page " + str(i)
        i += 1
        r = requests.get(url + str(i) + ".html")
        soup = BeautifulSoup(r.content, "html.parser")
        reading_area = soup.find_all("div", attrs={'class': 'dirwraps'})
        try:
            htmlparser = HTMLParser()
        except UnicodeEncodeError as e:
            print(e)

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


def download_books_from_csv(file_name):
    with open(file_name, 'rb') as csv_f:
        reader = csv.reader(csv_f, delimiter=',')
        for row in reader:
            bk_name = row[0]
            bk_link = row[1]
            start = time.clock()
            download_book("http://www.readromancebook.com/" + bk_link, website, bk_name)
            time_took = float(time.clock() - start)
            if time_took > 60:
                print bk_name + " Download took " + str(time_took / 60) + " Minutes"
            else:
                print bk_name + " Download took " + str(time_took) + " Seconds"


def download_book(book_url, web_site, book_name_s):
    bk_name = remove_disallowed_filename_chars(book_name_s)
    bk_name = bk_name.replace(' ', '_')
    # print "Downloading " + bk_name
    generated_url, tag, class_name, style_name = url_generator(web_site, book_url)
    book_content, error = scrape_book(generated_url, bk_name, tag, class_name, style_name)
    # if error:
    # print("Error Occurred!")
    write_convert_and_rename(book_content, bk_name)
    return bk_name + '.pdf', error


validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def remove_disallowed_filename_chars(filename):
    cleanedFilename = unicodedata.normalize('NFKD', unicode(filename)).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)


store_book_links_to_csv("http://www.readromancebook.com/books/", 78, "Books_Links_Final.csv")
download_books_from_csv("Books_Links_Final.csv")
