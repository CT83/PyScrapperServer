import os
import sys
from shutil import copy

import requests
from bs4 import BeautifulSoup

book_name = ""
os.chdir(sys.path[0])


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
    # print ("Url after Generation:" + url)
    return url


def scrape_book(url):
    print("Scrapping book at:" + url)
    error = False
    counter = 1
    iteration = 0
    book_text = ""
    try:
        while True or iteration < 2000:
            iteration += 1
            if counter == 1:
                r = requests.get(url[:-1] + ".html")
                # print("Page 1 Url:" + r.url)
            else:
                r = requests.get(url + str(counter) + ".html")
            if r.status_code == 200:  # Page Successfully Loaded
                book_text += "\n\nPage " + str(counter)
                soup = BeautifulSoup(r.content, "html.parser")
                reading_area = soup.find('div', attrs={'class': 'viewport', 'style': 'height:auto'})
                book_text += reading_area.text
                # print(book_text)
                # print("Scrapped Page: " + str(counter))
                counter = counter + 1
            elif r.status_code == 404:  # Reached End of Book
                break
            else:
                error = True
                print("Error has Occurred")
                break
            if iteration % 14 == 0:
                print("Scrapping Page:" + str(counter))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("Error :" + str(e))
        error = True
    return book_text, error


def main(book_url, website):
    if book_url == "" and website == "":
        book_url = "http://www.readromancebook.com/books/Devil_in_Texas.html"
        website = 'readromancebook.com'
    book, error = scrape_book(url_generator(website, book_url))
    f = open(book_name + '.txt', 'w')
    f.write(book.encode('ascii', 'ignore'))
    f.close()
    os.system('python txt2pdf.py ' + book_name + '.txt')
    os.rename('output.pdf', book_name + '.pdf')
    copy(book_name + '.pdf', 'path')
    os.remove(book_name + '.pdf')
    os.remove(book_name + '.txt')
    if error:
        print("Error Occurred!")
    return book_name + '.pdf', error


if __name__ == '__main__':
    main("", "")
