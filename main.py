from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(os.environ['CONFIGURATION_SETUP'])

@app.route('/')
def index():
    return 'Hello World' + str(app.config['MAIL_PORT'])

if __name__ == "__main__":
    app.run()