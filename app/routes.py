from flask import Flask, render_template, request
from flask_mail import Mail, Message
from pathlib import Path
from app.config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
import mysql.connector

app = Flask(__name__)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

mail = Mail(app)

def get_emails_from_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
	port="34106",
        user="ubuntu",
        password="@A172839a@",
        database="envio_desprendibles"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT email FROM usuario")
    emails = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return emails


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')  # Captura el asunto del formulario
        body = request.form.get('body')  # Captura el cuerpo del correo del formulario
                #subject = 'Envío de Archivos Adjuntos'
        #message = 'Este es un correo con archivos adjuntos'

        attachments = request.files.getlist('attachment')

        if attachments:
            msg = Message(subject, recipients=[email])
            msg.body = body

            # Adjuntar todos los archivos al mensaje
            for file in attachments:
                if file.filename:
                    filename = file.filename
                    upload_path = Path(__file__).parent / 'uploads' / filename
                    file.save(upload_path)
                    with open(upload_path, 'rb') as fp:
                        msg.attach(filename, 'application/octet-stream', fp.read())

            # Enviar el mensaje con todos los archivos adjuntos
            mail.send(msg)

            return 'Correo con archivos adjuntos enviado exitosamente'
        else:
            return 'No se han adjuntado archivos'

    emails = get_emails_from_database()

    return render_template('index.html', emails=emails)

