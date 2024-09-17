from flask import Flask, render_template, request, redirect, url_for, flash, session
import smtplib
from email.mime.text import MIMEText
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Get secret key from environment variable

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send the OTP to the user's email
def send_otp(email, otp):
    sender_email = os.getenv('SENDER_EMAIL')  # Get sender email from environment variable
    sender_password = os.getenv('SENDER_PASSWORD')  # Get sender password from environment variable
    msg = MIMEText(f'Your OTP code is: {otp}')
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("OTP sent successfully")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        otp = generate_otp()
        session['otp'] = otp
        session['email'] = email
        send_otp(email, otp)
        flash('OTP has been sent to your email. Please check your inbox.')
        return redirect(url_for('verify_otp'))
    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            flash('OTP verified successfully! Registration complete.')
            return redirect(url_for('register'))
        else:
            flash('Invalid OTP. Please try again.')
            return redirect(url_for('verify_otp'))
    return render_template('verify_otp.html')

if __name__ == '__main__':
    app.run(debug=True)
