## Amazon Price Tracker

### Sending mail in python

Refer [this](https://realpython.com/python-send-email/) doc.

1. Using SMTP_SSL()
```
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.login(os.environ.get("sender_email"), os.environ.get("password"))
server.sendmail(os.environ.get("sender_email"), os.environ.get("receiver_email"), message)
```

2. Using .starttls()
```
context = ssl.create_default_context()
erver = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls(context=context)
server.ehlo()
server.login(os.environ.get("sender_email"), os.environ.get("password"))
server.sendmail(os.environ.get("sender_email"), os.environ.get("receiver_email"), message)
server.quit()
```