from bs4 import BeautifulSoup, NavigableString
from requests_html_custom import request_html
import MySQLdb
import re
import requests
import time
import traceback
import random
import re
from bs4.element import Comment


def tag_visible(element, min_length):
    words_to_ignore_file = open("resources/words_dictionaries/words_to_ignore.txt", 'r')
    words_to_ignore_list = words_to_ignore_file.read().split(",")

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if len(element) < min_length:
        return False
    if not isinstance(element, NavigableString):
        return False
    if len(element.parent.findChildren("a", recursive=True)) > 25:
        return False
    if any(word.upper() in element.upper() for word in words_to_ignore_list):
        return False
    return True


def text_from_html(soup, min_length):
    texts = soup.findAll(text=True)
    visible_texts = filter(lambda element: tag_visible(element, min_length), texts)
    return u" ".join(t.strip() for t in visible_texts)


class YellowLabToolsError(Exception):
    """Base class for other exceptions"""
    pass


def parse_website_js(url):
    scrapping_results_dictionary = {
        'url': url
    }
    html = get_raw_html(url)
    soup = get_soup(html)
    get_text_related_data(scrapping_results_dictionary, soup)
    get_websites_references_data(scrapping_results_dictionary, soup)
    get_tag_counts_data(scrapping_results_dictionary, soup)
    get_total_code_length_data(scrapping_results_dictionary, html)

    file = open("js.html", "wb")
    file.write(html)

    parse_website_with_yellow_lab_tools(url, scrapping_results_dictionary, False)
    return scrapping_results_dictionary


def fill_database(result_dictionary, cursor, connection):
    cursor.execute(''' SELECT COUNT(*) FROM websites WHERE url = %s''', (result_dictionary['url'], ))
    result = cursor.fetchall()
    if result[0]['COUNT(*)'] > 0:
        print("Url already in database")
        return

    insert_statement = ''' INSERT INTO websites 
    (url, exclamation_count, words_to_avoid_count, smart_words_count, h1_count, h2_count,  div_count, iframe_count,
     a_count, img_count, p_count, span_count, button_count,
     input_count, form_count, script_count, meta_count, link_count, style_count,
     text_longer_than_50_characters_count, text_longer_than_100_characters_count, 
     text_longer_than_150_characters_count, text_longer_than_200_characters_count,
     http_references, https_references, total_code_length, ylt_DOMelementsCount, ylt_DOMelementMaxDepth,
      ylt_scriptDuration, ylt_jsErrors, ylt_cssColors, ylt_cssDuplicatedProperties, ylt_totalWeight, ylt_domains,
       ylt_compression, ylt_totalRequests, ylt_heavyFonts, ylt_global_score, ylt_badJavascript_score, ylt_jQuery_score,
        ylt_serverConfig_score)
     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.execute(insert_statement,
                   (result_dictionary['url'], result_dictionary['exclamation_count'],
                    result_dictionary['words_to_avoid_count'], result_dictionary['smart_words_count'],
                    result_dictionary['h1'], result_dictionary['h2'], result_dictionary['div'],
                    result_dictionary['iframe'], result_dictionary['a'], result_dictionary['img'],
                    result_dictionary['p'], result_dictionary['span'],
                    result_dictionary['button'], result_dictionary['input'], result_dictionary['form'],
                    result_dictionary['script'], result_dictionary['meta'], result_dictionary['link'],
                    result_dictionary['style'], result_dictionary['text_longer_than_50_characters_count'],
                    result_dictionary['text_longer_than_100_characters_count'],
                    result_dictionary['text_longer_than_150_characters_count'],
                    result_dictionary['text_longer_than_200_characters_count'],
                    result_dictionary['http_references'], result_dictionary['https_references'],
                    result_dictionary['total_code_length'], result_dictionary['ylt_DOMelementsCount'],
                    result_dictionary['ylt_DOMelementMaxDepth'], result_dictionary['ylt_scriptDuration'],
                    result_dictionary['ylt_jsErrors'], result_dictionary['ylt_cssColors'],
                    result_dictionary['ylt_cssDuplicatedProperties'], result_dictionary['ylt_totalWeight'],
                    result_dictionary['ylt_domains'], result_dictionary['ylt_compression'],
                    result_dictionary['ylt_totalRequests'], result_dictionary['ylt_heavyFonts'],
                    result_dictionary['ylt_global_score'], result_dictionary['ylt_badJavascript_score'],
                    result_dictionary['ylt_jQuery_score'], result_dictionary['ylt_serverConfig_score']))
    connection.commit()

    cursor.close()


def parse_website_with_yellow_lab_tools(url, scrapping_results_dictionary, using_docker=False):
    if using_docker:
        api_runs_endpoint = "http://localhost:8383/api/runs"
        api_result_endpoint = "http://localhost:8383/api/results"
    else:
        api_runs_endpoint = "https://yellowlab.tools/api/runs"
        api_result_endpoint = "https://yellowlab.tools/api/results"

    r = {}
    data = {
        "url": url
    }

    ylt_request_success = False

    headers = {
        'User-Agent': 'Fakenews platform',
        'x-api-key': 'X46CWs85bdJ37nBz'
    }

    try:
        r = requests.post(url=api_runs_endpoint, data=data, timeout=30, headers=headers)
        initial_response = r.json()
        time.sleep(15)
        while True:
            r = requests.get(url=api_runs_endpoint + f"/{initial_response['runId']}",
                             timeout=30, headers=headers)
            r = r.json()
            if r["status"]["statusCode"] == "complete":
                break
            time.sleep(10)
        r = requests.get(url=api_result_endpoint + f"/{initial_response['runId']}",
                         timeout=30, headers=headers).json()
        ylt_request_success = True
    except Exception as e:
        print(f"Error occured during YellowLabTools data fetching without using proxy:\n {traceback.format_exc()}"
              f"\nRequest status: {r.status_code} {r.reason}, request url: {r.url}\n")

    if not ylt_request_success:
        for x in range(10):
            proxy = random.choice(list(open('resources/http_proxies.txt'))).strip()
            proxy_dict = {
                "https": "http://" + proxy,
                "http": "http://" + proxy
            }
            try:
                r = requests.post(url=api_runs_endpoint, proxies=proxy_dict, data=data, timeout=30,
                                  headers={'User-Agent': 'Fakenews platform'})
                initial_response = r.json()
                time.sleep(10)
                while True:
                    r = requests.get(url=api_runs_endpoint + f"/{initial_response['runId']}",
                                                    proxies=proxy_dict, timeout=30,
                                     headers={'User-Agent': 'Fakenews platform'}).json()
                    if r["status"]["statusCode"] == "complete":
                        break
                    time.sleep(5)
                r = requests.get(url=api_result_endpoint + f"/{initial_response['runId']}",
                                              proxies=proxy_dict, timeout=30,
                                 headers={'User-Agent': 'Fakenews platform'}).json()
                ylt_request_success = True
                break
            except Exception as e:
                print(
                    f"Error occured during YellowLabTools data fetching using proxy {proxy}:"
                    f"\n{traceback.format_exc()}\n Request status: {r.status_code} {r.reason}. Try no. {x}\n")

        if not ylt_request_success:
            raise YellowLabToolsError("Cannot analyse given Url with Yellow Lab Tools")

    scrapping_results_dictionary['ylt_DOMelementsCount'] = r['rules']['DOMelementsCount']['value']
    scrapping_results_dictionary['ylt_DOMelementMaxDepth'] = r['rules']['DOMelementMaxDepth']['value']
    scrapping_results_dictionary['ylt_scriptDuration'] = r['rules']['scriptDuration']['value']
    scrapping_results_dictionary['ylt_jsErrors'] = r['rules']['jsErrors']['value']
    scrapping_results_dictionary['ylt_cssColors'] = r['rules']['cssColors']['value']
    scrapping_results_dictionary['ylt_cssDuplicatedProperties'] = \
        r['rules']['cssDuplicatedProperties']['value']
    scrapping_results_dictionary['ylt_totalWeight'] = r['rules']['totalWeight']['value']
    scrapping_results_dictionary['ylt_domains'] = r['rules']['domains']['value']
    scrapping_results_dictionary['ylt_compression'] = r['rules']['compression']['value']
    scrapping_results_dictionary['ylt_totalRequests'] = r['rules']['totalRequests']['value']
    scrapping_results_dictionary['ylt_heavyFonts'] = r['rules']['heavyFonts']['value']
    scrapping_results_dictionary['ylt_global_score'] = r['scoreProfiles']['generic']['globalScore']
    scrapping_results_dictionary['ylt_badJavascript_score'] = \
        r['scoreProfiles']['generic']['categories']['badJavascript']['categoryScore']
    scrapping_results_dictionary['ylt_jQuery_score'] = \
        r['scoreProfiles']['generic']['categories']['jQuery']['categoryScore']
    scrapping_results_dictionary['ylt_serverConfig_score'] = \
        r['scoreProfiles']['generic']['categories']['serverConfig']['categoryScore']


def get_cursor(mysql):
    return mysql.connection.cursor(MySQLdb.cursors.DictCursor)


def is_referencing_http(href):
    return href and re.compile("http://").search(href)


def is_referencing_https(href):
    return href and re.compile("https://").search(href)


def get_raw_html(url):
    session = request_html.HTMLSession()
    r = session.get(url)
    r.html.render(sleep=2, keep_page=True, scrolldown=1, timeout=50)
    html_raw = r.html.raw_html
    session.close()
    return html_raw


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_text_related_data(scrapping_results_dictionary, soup):
    smart_words_file = open("resources/words_dictionaries/smart_words.txt", 'r')
    words_to_avoid_file = open("resources/words_dictionaries/words_to_avoid.txt", 'r')

    smart_words_list = smart_words_file.read().split(",")
    words_to_avoid_list = words_to_avoid_file.read().split(",")

    text_concat = text_from_html(soup, 30)

    smart_words_count = sum(list(word in smart_words_list for word in text_concat.split()))
    words_to_avoid_count = sum(list(word in words_to_avoid_list for word in text_concat.split()))
    scrapping_results_dictionary['smart_words_count'] = smart_words_count
    scrapping_results_dictionary['words_to_avoid_count'] = words_to_avoid_count

    scrapping_results_dictionary['exclamation_count'] = len(re.findall(r"(\b[A-Z]{4,}\b|[?!])", text_concat))

    scrapping_results_dictionary['text_longer_than_50_characters_count'] = len(
        text_from_html(soup, 50))
    scrapping_results_dictionary['text_longer_than_100_characters_count'] = len(
        text_from_html(soup, 100))
    scrapping_results_dictionary['text_longer_than_150_characters_count'] = len(
        text_from_html(soup, 150))
    scrapping_results_dictionary['text_longer_than_200_characters_count'] = len(
        text_from_html(soup, 200))


def get_websites_references_data(scrapping_results_dictionary, soup):
    scrapping_results_dictionary['http_references'] = len(
        soup.find_all(href=is_referencing_http))
    scrapping_results_dictionary['https_references'] = len(
        soup.find_all(href=is_referencing_https))


def get_tag_counts_data(scrapping_results_dictionary, soup):
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


def get_total_code_length_data(scrapping_results_dictionary, html):
    scrapping_results_dictionary['total_code_length'] = len(html.decode())
