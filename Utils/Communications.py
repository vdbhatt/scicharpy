import smtplib


def send_email(email_address, subject, message):
    # prefer services like sendgrid etc..
    gmail_passwd = r'your pwd'
    gmail_sender = r'your email address'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % email_address,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % subject,
                        '', message])

    try:
        server.sendmail(gmail_sender, [email_address], BODY)
    except:
        print('error sending mail')

    server.quit()
    return
