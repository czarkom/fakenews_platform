from flask import Flask, render_template, request
import os
import json
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask_cors import CORS
from websiteParser import parse_website_js, fill_database, get_cursor

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['CONFIGURATION_SETUP'])
mysql = MySQL(app)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/search', methods=['POST'])
def search():
    request_data = request.get_json()
    website_stats = parse_website_js(request_data['url'])
    fill_database(website_stats, get_cursor(mysql), mysql.connection)

    return json.dumps(website_stats), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()