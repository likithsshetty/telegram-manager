from flask import Flask, request, redirect, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'user_db'
COLLECTION_NAME = 'users'
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
users = db[COLLECTION_NAME]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        telegram_id = request.form.get('telegram_id')
        if telegram_id:
            users.insert_one({'telegram_id': int(telegram_id)})
            return "Registration successful! You can now return to Telegram."
    # A simple HTML form for Telegram ID
    html_form = '''
        <form method="post">
            Telegram ID: <input type="text" name="telegram_id">
            <input type="submit" value="Sign Up">
        </form>
    '''
    return render_template_string(html_form)

@app.route('/')
def index():
    return redirect('/signup')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
