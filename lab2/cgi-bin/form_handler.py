#!/usr/bin/python3

import cgi
import cgitb
import os
from http import cookies

cgitb.enable()

form = cgi.FieldStorage()

cookie_str = os.environ.get('HTTP_COOKIE')
cookie = cookies.SimpleCookie()
cookie.load(cookie_str)

# Виправлення тут: правильне отримання значення з cookie
cookie_value = cookie.get('form_count')
count = int(cookie_value.value) if cookie_value else 0

if 'delete_cookies' in form:
    cookie['form_count'] = 0
    cookie['form_count']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    count = 0

if 'submit' in form:
    count += 1
    cookie['form_count'] = count

name = form.getvalue("name")
email = form.getvalue("email")
gender = form.getvalue("gender")
interests = form.getlist("interests")
country = form.getvalue("country")

print("Content-type: text/html")
print(cookie.output())
print()

print("<html>")
print("<head>")
print("<title>Form Submission Result</title>")
print("</head>")
print("<body>")
print("<h2>Form Submission Result</h2>")
print("<p><strong>Name:</strong> {}</p>".format(name))
print("<p><strong>Email:</strong> {}</p>".format(email))
print("<p><strong>Gender:</strong> {}</p>".format(gender))
print("<p><strong>Interests:</strong> {}</p>".format(", ".join(interests)))
print("<p><strong>Country:</strong> {}</p>".format(country))
print("<p>Number of forms submitted: {}</p>".format(count))
print('<p><a href="../index.html">Fill out a new form</a></p>')
print('<form method="POST">')
print('<input type="submit" name="submit" value="Submit Form">')
print('</form>')
print('<form method="POST">')
print('<input type="submit" name="delete_cookies" value="Delete Cookies">')
print('</form>')
print("</body>")
print("</html>")
