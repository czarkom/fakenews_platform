from bs4 import BeautifulSoup, NavigableString
from requests_html_custom import request_html
import MySQLdb


def parse_website_js(url, mysql):
    session = request_html.HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=10, timeout=40)
    webscrapping_results_dictionary = {}
    html = r.html.raw_html
    soup = BeautifulSoup(html, 'html.parser')
    div_count = soup.div
    webscrapping_results_dictionary['text_longer_than_100_characters_count'] = len(soup.find_all(string=is_the_only_string_within_a_tag))
    file = open("js.html", "wb")
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
        webscrapping_results_dictionary[tag] = len(soup_count)
    session.close()
    fill_database(url, webscrapping_results_dictionary, mysql)
    return webscrapping_results_dictionary


def fill_database(url, result_dictionary, mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(''' SELECT COUNT(*) FROM websites WHERE url = %s''', (url, ))
    result = cursor.fetchall()
    if result[0]['COUNT(*)'] > 0:
        print("Url already in database")
        return

    cursor.execute(''' INSERT INTO websites 
    (url, h1_count, h2_count,  div_count, iframe_count, a_count, span_count, button_count,
     input_count, form_count, script_count, meta_count, link_count, style_count)
     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                   (url, result_dictionary['h1'], result_dictionary['h2'], result_dictionary['div'],
                    result_dictionary['iframe'], result_dictionary['a'], result_dictionary['span'],
                    result_dictionary['button'], result_dictionary['input'], result_dictionary['form'],
                    result_dictionary['script'], result_dictionary['meta'], result_dictionary['link'],
                    result_dictionary['style']))
    mysql.connection.commit()

    cursor.close()


def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return s == s.parent.string and type(s) is NavigableString and len(s) > 100
