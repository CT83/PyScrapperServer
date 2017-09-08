import os
import requests
from bs4 import BeautifulSoup


def url_generator(ch, url):
    print url
    if ch == 'readromancebook.com':
        url = url[:-5]
        url += "/"
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


book = scrape_book(url_generator('readromancebook.com', "http://www.readromancebook.com/books/The_Reformed_Bad_Boys_Baby.html"))
f = open('FinalBook1.txt', 'w')
f.write(book.encode('ascii', 'ignore'))
f.close()
os.system('python txt2pdf.py FinalBook1.txt')
