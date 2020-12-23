import email
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union


class PostMan:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.GMAIL_SMTP = 'smtp.gmail.com'
        self.GMAIL_IMAP = 'imap.gmail.com'

    def mail_send(self, subject: str, recipients: Union[list, str], message: str):
        mail = MIMEMultipart()
        mail['From'] = self.login
        if isinstance(recipients, list):
            mail['To'] = ', '.join(recipients)
        else:
            mail['To'] = recipients
        mail['Subject'] = subject
        mail.attach(MIMEText(message))
        smtp_conn = smtplib.SMTP(self.GMAIL_SMTP, 587)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.ehlo()
        smtp_conn.login(self.login, self.password)
        smtp_conn.sendmail(self.login, smtp_conn, mail.as_string())
        smtp_conn.quit()

    def mail_receive(self, mail_folder='inbox', header=None):
        imap_conn = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        imap_conn.login(self.login, self.password)
        imap_conn.list()
        imap_conn.select(mail_folder)
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = imap_conn.uid('SEARCH', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = imap_conn.uid('FETCH', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        imap_conn.logout()
        return email_message
