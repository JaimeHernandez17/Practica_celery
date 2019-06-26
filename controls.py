import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from credentials import PASSWORD, EMAIL


class Controller:

    @staticmethod
    def create_or_update(type, message):
        f = open(f'{type}.txt', 'a+')
        f.write(f'{time.ctime()} - {message}\n')
        f.close()

    @staticmethod
    def send_email(type, message):
        msg = MIMEMultipart()
        message += f'\n{type}'
        password = PASSWORD
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        msg['Subject'] = "Rabbit"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        server.login(msg['From'], password)

        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()
