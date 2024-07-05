import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

server_smtp = 'smtp.gmail.com'
port = 587
sendermail = "italofarias071@gmail.com"
password = open('passwords/token', 'r').read()

from_em = 'italofarias071@gmail.com'
to_ = 'italofarias071@gmail.com'
assunto = 'Teste'
body = """
<p>
Teste de disparo de email com anexo
</p>
"""

mensagem = MIMEMultipart('alternative')
mensagem["From"] = from_em
mensagem["To"] = to_
mensagem["Subject"] = assunto
mensagem.attach(MIMEText(body,"html"))

xl = 'Valores_imagem.xlsx'
anexo = open(r'excel/Valores_imagem.xlsx','rb')



part = MIMEBase('aplication','octet-stream')
part.set_payload(anexo.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename={xl}')

mensagem.attach(part)
anexo.close()

server = None

try:
    server = smtplib.SMTP(server_smtp, port)
    server.starttls()


    server.login(sendermail, password)

    server.sendmail(sendermail, to_, mensagem.as_string())
    print("Email enviado")
except Exception as e:
    print(f"Houve um erro: {e}")
finally:
    if server:
        server.quit()