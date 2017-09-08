from bottle import get, post, request, run, route  # or route
from bottle import static_file
from Scrapper import main, book_name


@get('/')  # or @route('/login')
def homepage():
    return '''
        <form action="/download" method="post">
            URL: <input name="url" type="text" />
            Website: <input name="website" type="text" />
            <input value="Download" type="submit" />
        </form>
    '''


@post('/download')
def download():
    url = request.forms.get('url')
    website = request.forms.get('website')
    file = main(url, 'readromancebook.com')
    return "<a href='/static/out/" + file + "'>Download</a>"


@route('/static/out/<filename>')
def server_static(filename):
    return static_file(filename, root='path')


run(host='localhost', port=8080, debug=True, reloader=True)
