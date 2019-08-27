import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import Message

from aiohttp import web
from aiohttp_apispec import docs

from ..models.user import User


async def send_email(receiver_email, email_token):
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
            <a href="http://localhost:8000/api/email-confirmation/{0}">
                {0}
            </a>
            </p>
        </body>
    </html>
    """.format(email_token)

    msg.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        'smtp.gmail.com', 465, context=context
        ) as smtp_server:

        smtp_server.login(sender_email, password)
        
        smtp_server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )


@docs(tags=['Auth'], summary='Email confirmation')
async def set_active(request):

    user = await User.query.where(
        User.token == request.match_info.get('token')
    ).gino.first()
    
    if not user:
        return web.json_response(
            {"message": "Invalid token."}, status=401
        )
    
    await user.update(is_active=True).apply()

    return web.json_response(
            {'message': 'WELCOME'},
            status=200
        )