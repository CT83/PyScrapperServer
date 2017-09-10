import os
import sys

from bottle import get, post, request, run, route  # or route
from bottle import static_file

from Scrapper import main


@get('/')  # or @route('/login')
def homepage():
    return webpage


@route('/status', method='GET')
def result():
    pass


@post('/download')
def download():
    url = request.forms.get('url')
    website = request.forms.get('website')
    print("Submitted URL:" + url)
    print("Submitted Website:" + website)
    download_link, error = main(url, website)
    print("Download Link:" + download_link)
    # return template('download_status', name='Rohan')
    download_webpage = '''
    <html>
    <style>
    form {
        border: 3px solid #f1f1f1;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        cursor: pointer;
        width: 100%;
    }

    button:hover {
        opacity: 0.8;
    }

    .container {
        padding: 16px;
    }

    span.psw {
        float: right;
        padding-top: 16px;
    }

    /* Change styles for span and cancel button on extra small screens */
    @media screen and (max-width: 300px) {
        span.psw {
           display: block;
           float: none;
        }
     }
    </style>
    <body>

    <h2>Bottle Scrapper</h2>
    <form action=/static/out/''' + download_link + '''>
      <div class="container">
        <button value="Download" type="submit">Download</button>
      </div>
     </form>
    </body>
    </html>
    '''

    if error:
        return "<script>alert('An Error has Occurred! Please check your internet connection and Try again!');</script>"
    else:
        return download_webpage


@route('/static/out/<filename>')
def server_static(filename):
    return static_file(filename, root='path')


webpage = """
<html>
<style>
form {
    border: 3px solid #f1f1f1;
}

input[type=text], input[type=password] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    box-sizing: border-box;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
}

button:hover {
    opacity: 0.8;
}

.cancelbtn {
    width: auto;
    padding: 10px 18px;
    background-color: #f44336;
}

.imgcontainer {
    text-align: center;
    margin: 24px 0 12px 0;
}

img.avatar {
    width: 40%;
    border-radius: 50%;
}

.container {
    padding: 16px;
}

span.psw {
    float: right;
    padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
    span.psw {
       display: block;
       float: none;
    }
 }
</style>
<body>

<h2>Bottle Scrapper</h2>
<form action="/download" method="post">
  <div class="container">
    <label><b>Book</b></label>
    <input type="text" placeholder="Enter the Link of the Book" name="url" required>
    <label><b>Website</b></label>
    <select name="website">
    <option value="0">(please select:)</option>
    <option value="readromancebook.com" selected>www.readromancebook.com</option>
    <option value="2">two</option>
    <option value="3">three</option>
    <option value="other">other, please specify:</option>
    </select>

    <button value="Download" type="submit">Begin Scraping</button>
  </div>
 </form>
</body>
</html>

"""
os.chdir(sys.path[0])
run(host='0.0.0.0', port=8080, debug=True, reloader=True)
