
import ssl,smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


sender = 'wearecircleup@gmail.com'
receiver = 'danielnicolasmuner@gmail.com'
password = 'fjmn jryj zzcy ofuh'


message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["To"] = receiver
message["From"] = sender

# Create the plain-text and HTML version of your message
text = """
Hi,
How are you?"""

html = '<h1>Hola</h1>'

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)


context = ssl.create_default_context()
try:
  server = smtplib.SMTP_SSL(host="smtp.gmail.com",port=465,context=context)
  server.ehlo()
  server.login(sender,password)
  server.sendmail(from_addr=sender,to_addrs=receiver,msg=message.as_string())
except Exception as e:
  print(e)
finally:
  server.quit()