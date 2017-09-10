import os
import sys
from HTMLParser import HTMLParser

import requests
from bs4 import BeautifulSoup

from FileManagement import write_convert_and_rename

book_name = ""
os.chdir(sys.path[0])


def url_generator(ch, t_url):
    tag = ''
    class_name = ''
    style_name = ''
    global book_name
    if ch == 'readromancebook.com':
        t_url = t_url[:-5]
        t_url += "/"
        book_name = t_url
        y = book_name.replace("http://www.readromancebook.com/books/", '')
        book_name = y
        y = book_name.replace(".html", '')
        book_name = y
        book_name = book_name.rstrip('/')

        tag = "div"
        class_name = 'viewport'
        style_name = 'height:auto'

    if ch == 'offcampus.freebooks2017.org':
        # t_url = t_url[:-5]
        # t_url += "/"
        book_name = t_url
        y = book_name.replace("http://offcampus.freebooks2017.org/", '')
        book_name = y
        y = book_name.replace(".html", '')
        book_name = y
        book_name = book_name.rstrip('/')

        tag = "div"
        class_name = 'text'
        style_name = ''

    print ("Book Name:" + book_name)
    print ('t_url:' + t_url)
    print ('tag:' + tag)
    print ('class_name:' + class_name)
    print('style_name:' + style_name)
    return t_url, tag, class_name, style_name


def get_link_readromancebook_first(url):
    return requests.get(url[:-1] + ".html")


def get_link_readromancebook(url, counter):
    return requests.get(url + str(counter) + ".html")


def get_link_offcampus_first(url):
    return requests.get(url + "index.html")


def get_link_offcampus(url, counter):
    return requests.get(url + '/index_' + str(counter) + ".html")


def scrape_book(s_url, bk_name="", s_tag="div", s_class_name='viewport', s_style_name='height:auto'):
    print("Scrapping book at:" + s_url)
    error = False
    counter = 1
    iteration = 0
    book_text = ""
    try:
        while True or iteration < 2000:
            iteration += 1
            if counter == 1:
                # remove '/' and add .html to the page
                if 'readromancebook' in s_url:
                    r = get_link_readromancebook_first(s_url)
                    book_text += bk_name.replace('_', ' ') + '\n\n'  # Add Book title
                else:
                    r = get_link_offcampus_first(s_url)
                    book_text += bk_name + '\n\n'
            else:
                if 'readromancebook' in s_url:
                    r = get_link_readromancebook(s_url, counter)
                else:
                    r = get_link_offcampus(s_url, counter)
            if r.status_code == 200:  # Page Successfully Loaded
                soup = BeautifulSoup(r.content, "html.parser")
                reading_area = soup.find(s_tag, attrs={'class': s_class_name, 'style': s_style_name})
                htmlparser = HTMLParser()
                book_text += htmlparser.unescape(reading_area.text)
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
    generated_url, tag, class_name, style_name = url_generator(website, book_url)
    book_content, error = scrape_book(generated_url, book_name, tag, class_name, style_name)
    if error:
        print("Error Occurred!")
    write_convert_and_rename(book_content, book_name)
    return book_name + '.pdf', error


if __name__ == '__main__':
    main("", "")
