import requests
from bs4 import BeautifulSoup

url = "http://www.readromancebook.com/books/No_Weddings.html"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
reading_area = soup.find('div', attrs={'class': 'viewport', 'style': 'height:auto'})
print reading_area.text
