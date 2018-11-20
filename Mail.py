# If google is not letting you to sign in :-

# Go to this link and select Turn On
# https://www.google.com/settings/security/lesssecureapps

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def Send_Email(message, password):

    smtpObj = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    smtpObj.login(message['From'], password)
    smtpObj.sendmail(message['From'], message['To'], message.as_string())         
    print("Successfully sent email")

    smtpObj.quit()

# Use this format 
# message = MIMEMultipart()
# message['From'] = "sender email address"
# message['To'] = "receiver email address"

# message["Subject"] = "Subject"
# body = "This is just a test email"
# message.attach(MIMEText(body, 'html'))
# password = "password"

# Send_Email(message, password)

#Or simply use this

# sender = "sender email address"
# receiver = "receiver email address"
# password = "password"
# message = "This is just a test email"

# Send_Email(sender, receiver , message, password)