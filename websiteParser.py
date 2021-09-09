from bs4 import BeautifulSoup
from urllib import request
from requests_html import HTMLSession
from threading import Thread

def parse_website_js(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True,scrolldown=10)
    tags_dictionary = {}
    html = r.html.raw_html
    soup = BeautifulSoup(html, 'html.parser')
    file = open("js.txt", "wb")
    file.write(html)
    tag_array = ['div',
                 'h1',
                 'h2',
                 'iframe',
                 'a',
                 'span',
                 'i',
                 'button',
                 'input',
                 'form',
                 'meta',
                 'script',
                 'style',
                 'link']
    for tag in tag_array:
        soup_count = soup.find_all(tag)
        tags_dictionary[tag] = len(soup_count)
    session.close()
    print(tags_dictionary)


def parse_website(url, mysql):
    tags_dictionary = {}
    web_url = request.urlopen(url)
    html = web_url.read()
    file = open("html.txt", "wb")
    file.write(html)
    soup = BeautifulSoup(html, 'html.parser')
    tag_array = ['div', 'h1', 'h2', 'iframe', 'a', 'span', 'i', 'button', 'input', 'form', 'meta', 'script', 'style', 'link']
    for tag in tag_array:
        soup_count = soup.find_all(tag)
        tags_dictionary[tag] = len(soup_count)
    #fill_database(url, tags_dictionary, mysql)
    web_url.close()
    print(tags_dictionary)


def fill_database(url, result_dictionary, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO websites (url, h1_count, h2_count,  div_count, iframe_count, a_count, span_count)
     VALUES(%s, %s, %s, %s, %s, %s, %s)''',
                   (url, result_dictionary['h1'], result_dictionary['h2'], result_dictionary['div'],
                    result_dictionary['iframe'], result_dictionary['a'], result_dictionary['span']))
    mysql.connection.commit()
    cursor.close()