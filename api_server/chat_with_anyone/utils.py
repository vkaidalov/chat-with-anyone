import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(receiver_email, host, email_token):
    sender_email = 'chat0with0anyone@gmail.com'
    password = 'chat_admin'

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Confirmation'

    html = """
    <html>
        <head>`
            <h1>
                Finish registration by clicking the link below
            </h1>
        </head>
        <body>
            <p>The link below:<br>
            <a href="http://{0}/api/email-confirmation/{1}">
                {1}
            </a>
            </p>
        </body>
    </html>
    """.format(host, email_token)

    msg.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
            'smtp.gmail.com', 465, context=context
    ) as smtp_server:

        smtp_server.login(sender_email, password)

        smtp_server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
