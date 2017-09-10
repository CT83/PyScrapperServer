import os
import sys

import requests
from bs4 import BeautifulSoup

from FileManagement import write_convert_and_rename

book_name = ""
os.chdir(sys.path[0])


def url_generator(ch, url):
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


def scrape_book(url, bk_name=""):
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
                book_text += bk_name.replace('_', ' ') + '\n\n'
            else:
                r = requests.get(url + str(counter) + ".html")
            if r.status_code == 200:  # Page Successfully Loaded
                book_text += "\n\nPage " + str(counter)
                soup = BeautifulSoup(r.content, "html.parser")
                reading_area = soup.find('div', attrs={'class': 'viewport', 'style': 'height:auto'})
                book_text += reading_area.text
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
    book_content, error = scrape_book(url_generator(website, book_url), book_name)
    if error:
        print("Error Occurred!")
    write_convert_and_rename(book_content, book_name)
    return book_name + '.pdf', error


if __name__ == '__main__':
    main("", "")

