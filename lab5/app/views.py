import json
import os
import io
import platform
from datetime import datetime
import datetime
from flask import render_template, request, session, redirect, url_for, flash, make_response
from app import app, db
from app.forms import FeedbackForm
from app.models import Feedback
from app.forms import LoginForm  

app.secret_key = b'secret'

# Path to the JSON file containing user data
users_json_path = 'lab5/app/static/files/users.json' 

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
def contacts():
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

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data

        feedback = Feedback(name=name, comment=comment)

        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Відгук успішно надіслано', 'success')
        except:
            flash('Під час надсилання відгуку сталася помилка', 'error')

        return redirect(url_for('feedback'))

    feedback_data = Feedback.query.all()
    return render_template('feedback.html', form=form, feedback_data=feedback_data, common=common)

# Error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', common=common), 404

# Context processor to provide additional data to templates
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
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users_data:
            if users_data[username]['password'] == password:
                user_info = users_data[username]
                session['user_info'] = user_info
                flash('Ваші дані було збережено', 'success')  # Flash message for successful login
                return redirect(url_for('info'))
            else:
                flash('Невірний пароль', 'error')  # Flash message for incorrect password
        else:
            flash('Невірне імя користувача', 'error')  # Flash message for incorrect username

    if 'user_info' in session:
        flash('Ви вже увійшли', 'info')  # Flash message for already logged in
        return redirect(url_for('info'))


    return render_template('login.html', form=form, common=common)

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
