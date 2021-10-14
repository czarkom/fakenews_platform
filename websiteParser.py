from bs4 import BeautifulSoup, NavigableString
from requests_html_custom import request_html
import MySQLdb
import re


def parse_website_js(url):
    session = request_html.HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=10, timeout=40)
    scrapping_results_dictionary = {
        'url': url
    }
    html = r.html.raw_html
    soup = BeautifulSoup(html, 'html.parser')
    scrapping_results_dictionary['text_longer_than_100_characters_count'] = len(
        soup.find_all(string=is_the_only_within_tag_and_text_long_enough))
    scrapping_results_dictionary['http_references'] = len(
        soup.find_all(href=is_referencing_http))
    scrapping_results_dictionary['https_references'] = len(
        soup.find_all(href=is_referencing_https))
    scrapping_results_dictionary['total_code_length'] = len(html.decode())
    file = open("js.html", "wb")
    file.write(html)
    tag_array = ['div',
                 'h1',
                 'h2',
                 'iframe',
                 'p',
                 'a',
                 'img',
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
        scrapping_results_dictionary[tag] = len(soup_count)
    session.close()
    return scrapping_results_dictionary


def fill_database(result_dictionary, cursor, connection):
    cursor.execute(''' SELECT COUNT(*) FROM websites WHERE url = %s''', (result_dictionary['url'], ))
    result = cursor.fetchall()
    if result[0]['COUNT(*)'] > 0:
        print("Url already in database")
        return
    cursor.execute(''' INSERT INTO websites 
    (url, h1_count, h2_count,  div_count, iframe_count, a_count, img_count, p_count, span_count, button_count,
     input_count, form_count, script_count, meta_count, link_count, style_count, text_longer_than_100_characters_count,
     http_references, https_references, total_code_length)
     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                   (result_dictionary['url'], result_dictionary['h1'], result_dictionary['h2'], result_dictionary['div'],
                    result_dictionary['iframe'], result_dictionary['a'], result_dictionary['img'],
                    result_dictionary['p'], result_dictionary['span'],
                    result_dictionary['button'], result_dictionary['input'], result_dictionary['form'],
                    result_dictionary['script'], result_dictionary['meta'], result_dictionary['link'],
                    result_dictionary['style'], result_dictionary['text_longer_than_100_characters_count'],
                    result_dictionary['http_references'], result_dictionary['https_references'],
                    result_dictionary['total_code_length']))
    connection.commit()

    cursor.close()


def get_cursor(mysql):
    return mysql.connection.cursor(MySQLdb.cursors.DictCursor)


def is_referencing_http(href):
    return href and re.compile("http://").search(href)


def is_referencing_https(href):
    return href and re.compile("https://").search(href)


def is_the_only_within_tag_and_text_long_enough(s):
    """Return True if this string is the only child of its parent tag."""
    return s == s.parent.string and type(s) is NavigableString and len(s) > 100
