from websiteParser import parse_website_js, fill_database
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fakenews_platform"
)


def get_cursor():
    return mydb.cursor(dictionary=True)


with open('websites.txt', 'r') as websites_file:
    for line in websites_file:
        try:
            print(f"Parsing url: {line}")
            scrapping_result_dictionary = parse_website_js(line.rstrip())
            print(scrapping_result_dictionary)
            fill_database(scrapping_result_dictionary, get_cursor(), mydb)
        except Exception as e:
            print(f"Error occured while parsing url: {line}, error: {e}")

