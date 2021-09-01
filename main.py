from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.environ['CONFIGURATION_SETUP'])
mysql = MySQL(app)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def index():
    return render_template('home.html', template_folder="templates")


@app.route('/search', methods=['POST'])
def search():
    print(request.form)
    return "dupa"


if __name__ == "__main__":
    app.run()