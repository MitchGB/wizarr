from app.models.settings import SettingsGetModel, SettingsModel, SettingsPostModel
from app.models.database.settings import Settings

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_invitation_email(recipient: str, code: str) -> bool: 
    select_settings = Settings.select()
    settings = { setting.key: setting.value for setting in select_settings }

    smtp_address = settings["smtp_address"]
    smtp_port = settings["smtp_port"]
    smtp_username = settings["smtp_username"]
    smtp_password = settings["smtp_password"]


    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = "Mubie Invitation"
    html_content = f"""
    <html>
    <head>
        <style>
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #d03143; /* Bootstrap primary color */
                border: none;
                border-radius: 5px;
                text-align: center;
                text-decoration: none; /* Remove underline */
                transition: background-color 0.3s ease;
            }}

            .button:hover {{
                background-color: #0056b3; /* Darker shade on hover */
            }}
        </style>
    </head>
    <body>
        <h1>You have been invited to Mubie</h1>
        <p>Your invitation code is <strong>{code}</strong>.</p>

        <p>Visit <a href="https://accounts.mitchg.dev/i/{code}">https://accounts.mitchg.dev/i/{code}</a> or click the
        "Create Account" button to redeem this code</p>

        <a href="https://accounts.mitchg.dev/i/{code}" class="button">
            Create Account
        </a>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, 'html'))



    try:
        print("Sending email(s) sent successfully!")
        with smtplib.SMTP(smtp_address, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except Exception as e:
        return False


    return True