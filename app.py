import os
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, url_for, redirect, send_from_directory, request

MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]
MY_CELL = os.environ["MY_CELL"]


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['app_secretkey']

@app.route('/')
def home():  # put application's code here
    return render_template("index.html")


@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/download-resume')
def download_resume():
    return send_from_directory('static', path='files/Josh Maitre Resume.pdf')


@app.route('/contact')
def contact():
    return render_template("contact.html")


def send_contact_info(name, email, phone, message):
    msg = EmailMessage()
    msg["From"] = MY_EMAIL
    msg["To"] = MY_CELL
    msg["Subject"] = f"🚨New Contact Form"
    msg.set_content(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.send_message(msg)
        print("email sent")


@app.route('/contact', methods=["POST"])
def receive_data():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    send_contact_info(name, email, phone, message)
    return redirect(url_for('contact'))


@app.route('/projects')
def projects():
    return render_template('projects.html')


if __name__ == '__main__':
    app.run(debug=True)
