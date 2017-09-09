# PyScrapperServer
This script is a Python Scrapper  controlled vai a Web Interface which uses Bottle;  BeautifulSoup 4  is used for scrapping EBooks off Websites which host them for free.

<b>Preface</b>
This project was entirely created on a Friday when I called in sick from College. This project provided  me an  introduction to Web Servers, Web Frameworks, Scrapping in Python and the Bottle Framework. 

<b>Introduction</b>
The code is run on a Raspberry Pi connected to the local WiFi connection, preferably using  a Static IP. The user accesses the Web Interfaces hosted on the Pi and then pastes the link of the EBook that he wishes to download. The Ebook is then scrapped off the Link provided by the user. It is further converted to PDF format for easy reading.
<em><b>tl;dr</b>&nbsp;  Web Server which Scrapes the Web.</em>

<b>How to Install?</b>
1. Clone this Repo
2. Install Dependencies  <br/>`sudo pip install reportlab requests bs4 python-dev install bottle`
3. `sudo nano /etc/rc.local`
4. Add  `sudo python path_of_this_cloned_repo/BottleServer.py`  to the end of the file before  `exit 0` , to allow the server to run at boot.
5. `sudo reboot`

Done!
Now visit the IP Address of the Server  example`192.168.1.10:8080`


<b>Dependencies</b>
1. [txt2pdf](https://github.com/baruchel/txt2pdf%22txt2pdf%22)
2. [bottle](https://github.com/bottlepy/bottle%22bottle%22)
3. [reportlab](https://github.com/Distrotech/reportlab)
4. [Beautiful Soup](https://code.launchpad.net/beautifulsoup)
5. [requests](https://github.com/requests/requests)

<b>Conclusion</b>
This project successfully downloaded several Ebooks from Websites and so was a succcess.
