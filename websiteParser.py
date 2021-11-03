from bs4 import BeautifulSoup, NavigableString
from requests_html_custom import request_html
import MySQLdb
import re
import requests
import json
import time
import traceback

class YellowLabToolsError(Exception):
    """Base class for other exceptions"""
    pass

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

    parse_website_with_yellow_lab_tools(url, scrapping_results_dictionary)
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
     http_references, https_references, total_code_length, ylt_DOMelementsCount, ylt_DOMelementMaxDepth,
      ylt_scriptDuration, ylt_jsErrors, ylt_cssColors, ylt_cssDuplicatedProperties, ylt_totalWeight, ylt_domains,
       ylt_compression, ylt_totalRequests, ylt_heavyFonts, ylt_global_score, ylt_badJavascript_score, ylt_jQuery_score,
        ylt_serverConfig_score)
     VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                   (result_dictionary['url'], result_dictionary['h1'], result_dictionary['h2'], result_dictionary['div'],
                    result_dictionary['iframe'], result_dictionary['a'], result_dictionary['img'],
                    result_dictionary['p'], result_dictionary['span'],
                    result_dictionary['button'], result_dictionary['input'], result_dictionary['form'],
                    result_dictionary['script'], result_dictionary['meta'], result_dictionary['link'],
                    result_dictionary['style'], result_dictionary['text_longer_than_100_characters_count'],
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


def parse_website_with_yellow_lab_tools(url, scrapping_results_dictionary):
    API_RUNS_ENDPOINT = "https://yellowlab.tools/api/runs"
    API_RESULT_ENDPOINT = "https://yellowlab.tools/api/results"

    r = {}
    data = {
        "url": url
    }

    ylt_request_success = False

    try:
        r = requests.post(url=API_RUNS_ENDPOINT, data=data, timeout=30)
        initial_response = r.json()
        time.sleep(10)
        while True:
            r = requests.get(url=API_RUNS_ENDPOINT + f"/{initial_response['runId']}",
                                            timeout=30).json()
            if r["status"]["statusCode"] == "complete":
                break
            time.sleep(5)
        r = requests.get(url=API_RESULT_ENDPOINT + f"/{initial_response['runId']}",
                                      timeout=30).json()
        ylt_request_success = True
    except Exception as e:
        print(f"Error occured during YellowLabTools data fetching without using using proxy:\n {traceback.format_exc()}"
              f"\nRequest status: {r.text}, request url: {r.url}\n")

    if not ylt_request_success:
        with open("resources/http_proxies.txt", encoding="utf-8", mode="r") as f:
            for proxy in f:
                proxy_dict = {
                    "https": "http://" + proxy.strip(),
                    "http": "http://" + proxy.strip()
                }
                try:
                    r = requests.post(url=API_RUNS_ENDPOINT, proxies=proxy_dict, data=data, timeout=30)
                    initial_response = r.json()
                    time.sleep(10)
                    while True:
                        r = requests.get(url=API_RUNS_ENDPOINT + f"/{initial_response['runId']}",
                                                        proxies=proxy_dict, timeout=30).json()
                        if r["status"]["statusCode"] == "complete":
                            break
                        time.sleep(5)
                    r = requests.get(url=API_RESULT_ENDPOINT + f"/{initial_response['runId']}",
                                                  proxies=proxy_dict, timeout=30).json()
                    ylt_request_success = True
                    break
                except Exception as e:
                    print(
                        f"Error occured during YellowLabTools data fetching using proxy {proxy.strip()}:"
                        f"\n{traceback.format_exc()}\n Request status: {r.text}\n")

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


def is_the_only_within_tag_and_text_long_enough(s):
    """Return True if this string is the only child of its parent tag."""
    return s == s.parent.string and type(s) is NavigableString and len(s) > 100
