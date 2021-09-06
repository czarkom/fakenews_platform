from bs4 import BeautifulSoup
from urllib import request


def parse_website(url):
    tags_dictionary = {}
    web_url = request.urlopen(url)
    html = web_url.read()
    soup = BeautifulSoup(html, 'html.parser')
    print(html)
    tag_array = ['div', 'h1', 'h2', 'iframe', 'a', 'span', 'i', 'button', 'input', 'form', 'meta', 'script', 'style', 'link']
    for tag in tag_array:
        soup_count = soup.find_all(tag)
        tags_dictionary[tag] = len(soup_count)

    print(tags_dictionary)


def fill_database(result_dictionary):
    print("hejka")