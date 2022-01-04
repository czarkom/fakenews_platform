from flask import Flask, render_template, request
import os
import json
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask_cors import CORS
from websiteParser import parse_website_js, fill_database, get_cursor
import predicting as pd
import pandas as pds
import numpy as np

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['CONFIGURATION_SETUP'])
mysql = MySQL(app)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/analyze', methods=['POST'])
def search():
    request_data = request.get_json()
    website_stats = pd.predict_random(request_data['url'], 'models/acc70_binary')
    # fill_database(website_stats, get_cursor(mysql), mysql.connection)
    website_stats['statistics'] = get_stats()
    return json.dumps(website_stats), 200, {'ContentType': 'application/json'}


@app.route('/data', methods=['GET'])
def get_data():
    cursor = get_cursor(mysql)
    cursor.execute(''' SELECT * FROM websites''')
    data = cursor.fetchall()
    return json.dumps(data), 200, {'ContentType': 'application/json'}


def get_stats():
    cursor = get_cursor(mysql)
    cursor.execute(''' SELECT * FROM websites''')
    data = list(cursor.fetchall())
    df = pds.DataFrame(data)
    df.set_index('id', inplace=True)
    stats = df.describe(include=[np.number]).to_json()
    return stats


if __name__ == "__main__":
    app.run()