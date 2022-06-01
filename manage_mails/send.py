import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from manage_mails.text import html_text

class Sender:

    def __init__(self):
        self.sender = "to-mayak@mail.ru"
        self.password = "L86PUUzBTY6NKxXybFs4"

    def send_socio_psych(self, subject, _from, email, content):

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = "to-mayak@mail.ru"
        msg["To"] = "drobkov155099@gmail.com"
        msg['Message-ID'] = make_msgid()
        msg["Content"]

        text = MIMEText(html_text.replace("{{subject}}", subject).replace("{{telefon}}", _from).replace("{{content}}", content).replace("{{email}}", email), "html")

        server = smtplib.SMTP("smtp.mail.ru", 587)
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, msg["To"], text.as_string())

    def send_yurist(self, subject, _from, email, content):
        pass

#if __name__ == "__main__":
    #Sender().send("Социально-психологическая помощь", "897...", "123456@gmail.com", "Оставляем заявку на сайте, нужна помощь по тому то, тому то.")