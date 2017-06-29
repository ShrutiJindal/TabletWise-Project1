import smtplib
from email import MIMEMultipart
from email import MIMEText
from email import MIMEBase
from email import encoders

def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):

    fromaddr = send_from
    toaddr = send_to
    msg = MIMEMultipart.MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Some domains have changed links"

    body = "PFA the list of the domain"

    msg.attach(MIMEText.MIMEText(body, 'plain'))

    attachment = open(files, "rb")

    part = MIMEBase.MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % files)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ENTER PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
