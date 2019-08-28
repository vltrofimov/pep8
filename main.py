import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailWork:
    def __init__(self,login,password,send_server,receive_server):
        self.login=login
        self.password=password
        self.send_server=send_server
        self.receive_server=receive_server

    def sendmessage(self,subject,header,message,*args):
        self.subject=subject
        self.header=header
        self.message=message
        self.args=args

        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.args)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))

        ms = smtplib.SMTP(self.send_server, 465)  # identify ourselves to smtp yandex client
        ms.ehlo()   # secure our email with tls encryption
        ms.starttls() #re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login,
        ms, msg.as_string())
        ms.quit()

    def receivemessage(self):
        mail = imaplib.IMAP4_SSL(self.receive_server)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()


if __name__ == '__main__':
    mailwork=MailWork('vltrofimov32@yandex.ru','P@ssw0rd32','smtp.yandex.ru','imap.yandex.ru')
    mailwork.sendmessage('Subject', 'None', 'Message','vltrofimov@gmail.com')
    mailwork.receivemessage()