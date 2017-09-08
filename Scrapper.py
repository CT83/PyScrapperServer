import os
from shutil import copy

import requests
from bs4 import BeautifulSoup

book_name = ""


def url_generator(ch, url):
    print url
    if ch == 'readromancebook.com':
        url = url[:-5]
        url += "/"
        global book_name
        book_name = url
        y = book_name.replace("http://www.readromancebook.com/books/", '')
        book_name = y
        y = book_name.replace(".html", '')
        book_name = y
        book_name = book_name.rstrip('/')

    print ("Book Name:" + book_name)
    print ("Url after Generation:" + url)
    return url


def scrape_book(url):
    counter = 1
    book_text = ""
    r = requests
    while True:
        if counter == 1:
            r = requests.get(url[:-1] + ".html")
            print("Page 1 Url:" + r.url)
        else:
            r = requests.get(url + str(counter) + ".html")
        if r.status_code == 200:
            book_text += "\n\nPage " + str(counter)
            soup = BeautifulSoup(r.content, "html.parser")
            reading_area = soup.find('div', attrs={'class': 'viewport', 'style': 'height:auto'})
            book_text += reading_area.text
            # print(book_text)
            print("Scrapped Page: " + str(counter))
            counter = counter + 1
        else:
            break
    print("Done Scrapping!")
    return book_text


def main(book_url, website):
    if book_url == "" and website == "":
        book_url = "http://www.readromancebook.com/books/Devil_in_Texas.html"
        website = 'readromancebook.com'
    book = scrape_book(url_generator(website, book_url))
    f = open(book_name + '.txt', 'w')
    f.write(book.encode('ascii', 'ignore'))
    f.close()
    os.system('python txt2pdf.py ' + book_name + '.txt')
    os.rename('output.pdf', book_name + '.pdf')
    copy(book_name + '.pdf', 'path')
    print("File Copied to Path...")
    os.remove(book_name + '.pdf')

    return book_name + '.pdf'


if __name__ == '__main__':
    main("", "")
