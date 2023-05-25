import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import AppCongiuration


def send_email(email_body, email_subject):
    app_initiate = AppCongiuration()
    app_config = app_initiate.load_app_config_settings()
    if app_config.sender_email_id is not None:
        message = MIMEMultipart("alternative")
        message["Subject"] = email_subject
        message["From"] = app_config.sender_email_id
        message["To"] = app_config.receiver_email_id

        # Create the plain-text and HTML version of your message
        html = f"""\
        <html>
        <body>
            <p>Hi,<br><br>
            {email_body}
            </p>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(app_config.sender_email_id, app_config.email_auth)
                server.sendmail(
                    app_config.sender_email_id, app_config.receiver_email_id, message.as_string()
                )
        except Exception as ex:
            print(f'Failed to send email: {ex}')


