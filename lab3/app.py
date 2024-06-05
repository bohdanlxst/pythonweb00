import datetime
import io
import json
import os
import platform

from flask import Flask, render_template, request

app = Flask(__name__)

common = {
    'first_name': 'Bohdan',
    'last_name': 'Ivaniuk',
}


@app.route('/')
def index():
    return render_template('home.html', common=common)


@app.route('/about')
def biography():
    return render_template('about.html', common=common)


@app.route('/skills')
def skills():
    data = get_static_json("static/files/skills.json")
    return render_template('skills.html', common=common, data=data)


@app.route('/contact')
def projects():
    return render_template('contact.html', common=common)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', common=common), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    with open(get_static_file(path), "r", encoding="utf-8") as file:
        return json.load(file)
    
@app.context_processor
def utility_processor():
    os_info = platform.platform()
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    return {
        'os_info': os_info,
        'user_agent': user_agent,
        'current_time': current_time
    }

if __name__ == "__main__":
    print("Running the web app")
    app.run(host="127.0.0.1", port=5000, debug=True)
