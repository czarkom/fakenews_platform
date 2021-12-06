from websiteParser import get_text_related_data, get_raw_html, get_soup
import mysql.connector
import traceback

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fakenews_platform"
)


def get_cursor():
    return mydb.cursor(dictionary=True)


def update_text_related_columns():
    cursor = get_cursor()
    try:
        cursor.execute(''' SELECT * FROM websites''')
        result = cursor.fetchall()
        for entry in result:
            url = entry['url']
            try:
                print(f"Updating text data related to url: {url}")
                scrapping_results_dictionary = {
                    'url': url
                }
                html = get_raw_html(url)
                soup = get_soup(html)
                get_text_related_data(scrapping_results_dictionary, soup)

                update_statement = ''' UPDATE websites 
                set exclamation_count = %s,
                words_to_avoid_count = %s,
                smart_words_count = %s,
                text_longer_than_50_characters_count = %s,
                text_longer_than_100_characters_count = %s,
                text_longer_than_150_characters_count = %s,
                text_longer_than_200_characters_count = %s 
                where url = %s'''

                cursor.execute(update_statement,
                               (
                                   scrapping_results_dictionary['exclamation_count'],
                                   scrapping_results_dictionary['words_to_avoid_count'],
                                   scrapping_results_dictionary['smart_words_count'],
                                   scrapping_results_dictionary['text_longer_than_50_characters_count'],
                                   scrapping_results_dictionary['text_longer_than_100_characters_count'],
                                   scrapping_results_dictionary['text_longer_than_150_characters_count'],
                                   scrapping_results_dictionary['text_longer_than_200_characters_count'],
                                   url
                               )
                               )
                mydb.commit()
                print(scrapping_results_dictionary)
            except Exception as e:
                print(f"Error occured while updating url {url}: {traceback.format_exc()}")
    except Exception as e:
        print(f"Error occured while text related data update: {traceback.format_exc()}")


update_text_related_columns()
