import time
import smtplib
import ssl
from pathlib import Path
from email.message import EmailMessage

# Configuracion del laboratorio
DESTINO = input("Correo destinatario de prueba: ")
REMITENTE = input("Correo Gmail remitente: ")
APP_PASSWORD = input("Contrasena de aplicacion de Gmail: ")

ARCHIVO = Path("variables.py")

# Crear archivo de prueba
ARCHIVO.write_text(
    "INFORME DE LABORATORIO TERMUX\n"
    "Prueba de envio de archivos adjuntos.\n",
    encoding="utf-8"
)

# Contexto SSL
contexto = ssl.create_default_context()

# Bucle automatico
contador = 0

try:
    while True:

        msg = EmailMessage()
        msg["From"] = REMITENTE
        msg["To"] = DESTINO
        msg["Subject"] = "Prueba de archivo adjunto Termux"

        msg.set_content("Adjunto informe de diagnostico.")

        datos = ARCHIVO.read_bytes()

        msg.add_attachment(
            datos,
            maintype="text",
            subtype="plain",
            filename=ARCHIVO.name
        )

        # Envio real por SMTP de Gmail
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
                smtp.login(REMITENTE, APP_PASSWORD)
                smtp.send_message(msg)
            estado = "enviado OK"
        except Exception as e:
            estado = f"ERROR: {e}"

        contador += 1

        print(f"Prueba numero: {contador}")
        print(f"Archivo adjunto preparado correctamente -> {estado}")
        print("Esperando 2 segundos...")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nLaboratorio detenido.")
    print(f"Total de pruebas: {contador}")
