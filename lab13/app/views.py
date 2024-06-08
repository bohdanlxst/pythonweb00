import json
import os
import io
import platform
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import FeedbackForm, TodoForm, LoginForm, ChangePasswordForm, RegistrationForm
from app.models import Feedback, Todo, User, db
from flask import Blueprint
from .models import Feedback, Todo, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)
    
@main_bp.route('/about')
def about():
    return render_template('about.html')
main_bp = Blueprint('main', __name__)

app = Flask(__name__)
app.secret_key = b'secret'
user_session = {}

# Path to the JSON file containing user data
users_json_path = 'lab13/app/static/files/users.json'

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
    current_time = datetime.now()
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful", category="success")
            return redirect(url_for("info"))

        flash("Invalid email or password", category="danger")
        return redirect(url_for("login"))

    return render_template('login.html', form=form, common=common)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", "success")
            return redirect(url_for("login"))
        except:
            db.session.rollback()
            flash("ERROR, try use another data", category="danger")
            return redirect(url_for("registration"))

    return render_template("register.html", form=form, common=common)

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    form = ChangePasswordForm() 

    if current_user.is_authenticated:
        email = current_user.email
        cookies = []

        if request.method == 'POST':
            if 'cookie_key' in request.form and 'cookie_value' in request.form and 'cookie_expiration' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiration = int(request.form['cookie_expiration'])

                response = make_response(redirect(url_for('info')))
                response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiration)
                session[f'cookie_creation_{cookie_key}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                flash(f"Cookie '{cookie_key}' added successfully.", 'success')

            if 'delete_cookie_key' in request.form:
                delete_cookie_key = request.form['delete_cookie_key']

                if delete_cookie_key in request.cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(delete_cookie_key)
                    session.pop(f'cookie_creation_{delete_cookie_key}', None)
                    flash(f"Cookie '{delete_cookie_key}' deleted successfully.", 'success')

            if 'delete_all_cookies' in request.form:
                response = make_response(redirect(url_for('info')))
                for key in request.cookies:
                    response.delete_cookie(key)
                    session.pop(f'cookie_creation_{key}', None)
                flash("All cookies deleted successfully.", 'success')

            return response

        return render_template('info.html', email=email, cookies=cookies, common=common, form=form)

    else:
        flash("You are not logged in. Please log in to access this page.", "error")
        return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' in user_session:
        if request.method == 'POST':
            cookie_key = request.form.get('cookie_key')
            cookie_value = request.form.get('cookie_value')
            cookie_expiration = int(request.form.get('cookie_expiration'))

            response = make_response(redirect(url_for('info')))
            response.set_cookie(cookie_key, cookie_value, max_age=cookie_expiration)
            session[f'cookie_creation_{cookie_key}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            flash(f"Cookie '{cookie_key}' added successfully.", 'success')

            return response
        else:
            return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' in user_session:
        if request.method == 'POST':
            if 'delete_cookie_key' in request.form:
                delete_cookie_key = request.form['delete_cookie_key']

                if delete_cookie_key in request.cookies:
                    response = make_response(redirect(url_for('info')))
                    response.delete_cookie(delete_cookie_key)
                    session.pop(f'cookie_creation_{delete_cookie_key}', None)
                    flash(f"Cookie '{delete_cookie_key}' deleted successfully.", 'success')

                    return response

        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' in user_session:
        if request.method == 'POST':
            response = make_response(redirect(url_for('info')))
            for key in request.cookies:
                response.delete_cookie(key)
                session.pop(f'cookie_creation_{key}', None)
            flash("All cookies deleted successfully.", 'success')

            return response
        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST' or request.method == 'GET':
        logout_user()
        flash("You've been logged out", category="success")
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@app.route('/change_password', methods=['POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user

        if user and user.verify_password(form.old_password.data):
            try:
                user.password = form.new_password.data
                db.session.commit()
                flash("Password changed", category="success")
            except:
                db.session.rollback()
                flash("Error", category="danger")
        else:
            flash("Error", category="danger")
    else:
        flash("Error", category="danger")

    return redirect(url_for('info'))

@app.route('/todo')
def home():
    todo_list = db.session.query(Todo).all()
    form = TodoForm()  
    return render_template("todo.html", todo_list=todo_list, form=form, common=common)

@app.route("/add", methods=["POST"])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/users')
def users():
    return render_template('users.html', users=User.query.all())

@app.route('/account')
@login_required
def account():
    form = ChangePasswordForm()
    return render_template('account.html', form=form, user=current_user, is_authenticated=True, title='Account')

if __name__ == '__main__':
    app.run(debug=True)
