<<<<<<< HEAD
import json
import os
import platform
import datetime
import io
from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = b'secret'

# Path to the JSON file containing user data
users_json_path = 'lab4/static/files/users.json' 

# Load user data from the JSON file
with open(users_json_path, 'r') as users_file:
    users_data = json.load(users_file)

# Function to save user data to the JSON file
def save_users_data():
    with open(users_json_path, 'w') as users_file:
        json.dump(users_data, users_file, indent=4)

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

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_data:
            if users_data[username]['password'] == password:
                user_info = users_data[username]
                session['user_info'] = user_info
                flash('Успішний вхід', 'success')
                return redirect(url_for('info'))
            else:
                flash('Невірний пароль', 'error')
        else:
            flash('Невірне імя користувача', 'error')

    if 'user_info' in session:
        flash('Ви вже увійшли', 'info')
        return redirect(url_for('info'))

    return render_template('login.html', common=common)

# Route for the user info page
@app.route('/info', methods=['GET', 'POST'])
def info():
    user_info = session.get('user_info')

    if request.method == 'POST':
        action = request.form.get('action')

        if user_info:
            if action == 'logout':
                session.pop('user_info', None)
                flash('Ви успішно вийшли з системи', 'success')
                return redirect(url_for('login'))

            elif action == 'change_password':
                new_password = request.form.get('new_password')

                if not new_password:
                    flash('Відсутній новий пароль', 'error')
                    return redirect(url_for('info'))

                users_data[user_info['username']]['password'] = new_password

                save_users_data()
                flash('Пароль успішно змінено', 'success')

            elif action == 'add_cookie':
                cookie_key = request.form.get('cookie_key')
                cookie_value = request.form.get('cookie_value')
                expire_time = request.form.get('cookie_expire_time')

                if not cookie_key or not cookie_value:
                    flash('Відсутній ключ або значення cookie', 'error')
                elif not expire_time.isnumeric():
                    flash('Недійсний термін дії', 'error')
                else:
                    expire_time = int(expire_time)
                    response = make_response(render_template('info.html', common=common, user_info=user_info))
                    response.set_cookie(cookie_key, cookie_value, max_age=expire_time)
                    flash('Файл cookie успішно додано', 'success')
                    return response

            elif action == 'delete_cookie':
                cookie_key_delete = request.form.get('cookie_key_delete')
                if cookie_key_delete:
                    response = make_response(render_template('info.html', common=common, user_info=user_info))
                    response.delete_cookie(cookie_key_delete)
                    flash('Файл cookie успішно видалено', 'success')
                    return response
                else:
                    flash('Відсутній ключ cookie', 'error')

    if user_info:
        return render_template('info.html', common=common, user_info=user_info)
    else:
        flash('Ви повинні увійти, щоб отримати доступ до цієї сторінки', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
=======
import json
import os
import platform
import datetime
import io
from flask import Flask, request, render_template, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = b'secret'

# Path to the JSON file containing user data
users_json_path = 'lab4/static/files/users.json' 

# Load user data from the JSON file
with open(users_json_path, 'r') as users_file:
    users_data = json.load(users_file)

# Function to save user data to the JSON file
def save_users_data():
    with open(users_json_path, 'w') as users_file:
        json.dump(users_data, users_file, indent=4)

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

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_data:
            if users_data[username]['password'] == password:
                user_info = users_data[username]
                session['user_info'] = user_info
                flash('Успішний вхід', 'success')
                return redirect(url_for('info'))
            else:
                flash('Невірний пароль', 'error')
        else:
            flash('Невірне імя користувача', 'error')

    if 'user_info' in session:
        flash('Ви вже увійшли', 'info')
        return redirect(url_for('info'))

    return render_template('login.html', common=common)

# Route for the user info page
@app.route('/info', methods=['GET', 'POST'])
def info():
    user_info = session.get('user_info')

    if request.method == 'POST':
        action = request.form.get('action')

        if user_info:
            if action == 'logout':
                session.pop('user_info', None)
                flash('Ви успішно вийшли з системи', 'success')
                return redirect(url_for('login'))

            elif action == 'change_password':
                new_password = request.form.get('new_password')

                if not new_password:
                    flash('Відсутній новий пароль', 'error')
                    return redirect(url_for('info'))

                users_data[user_info['username']]['password'] = new_password

                save_users_data()
                flash('Пароль успішно змінено', 'success')

            elif action == 'add_cookie':
                cookie_key = request.form.get('cookie_key')
                cookie_value = request.form.get('cookie_value')
                expire_time = request.form.get('cookie_expire_time')

                if not cookie_key or not cookie_value:
                    flash('Відсутній ключ або значення cookie', 'error')
                elif not expire_time.isnumeric():
                    flash('Недійсний термін дії', 'error')
                else:
                    expire_time = int(expire_time)
                    response = make_response(render_template('info.html', common=common, user_info=user_info))
                    response.set_cookie(cookie_key, cookie_value, max_age=expire_time)
                    flash('Файл cookie успішно додано', 'success')
                    return response

            elif action == 'delete_cookie':
                cookie_key_delete = request.form.get('cookie_key_delete')
                if cookie_key_delete:
                    response = make_response(render_template('info.html', common=common, user_info=user_info))
                    response.delete_cookie(cookie_key_delete)
                    flash('Файл cookie успішно видалено', 'success')
                    return response
                else:
                    flash('Відсутній ключ cookie', 'error')

    if user_info:
        return render_template('info.html', common=common, user_info=user_info)
    else:
        flash('Ви повинні увійти, щоб отримати доступ до цієї сторінки', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 120de884db0d88ae4107c797f5b9917b11c7b18a
