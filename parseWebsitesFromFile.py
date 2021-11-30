from websiteParser import parse_website_js, fill_database
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


with open('resources/training_data/not_that_legit.txt', 'r') as websites_file:
    cursor = get_cursor()
    for line in websites_file:
        try:
            print(f"Parsing url: {line.strip()}")
            cursor.execute(''' SELECT COUNT(*) FROM websites WHERE url = %s''', (line.strip(),))
            result = cursor.fetchall()
            if result[0]['COUNT(*)'] > 0:
                print("Url already in database")
                continue
            scrapping_result_dictionary = parse_website_js(line.rstrip())
            print(scrapping_result_dictionary)
            fill_database(scrapping_result_dictionary, get_cursor(), mydb)
        except Exception as e:
            print(f"Error occured while parsing url: {line.strip()}, error: {e}, stacktrace: {traceback.format_exc()}")

