from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from pathlib import Path
from app.config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
import mysql.connector
from flask import jsonify

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

@app.route('/templates')
def success():
    return render_template('success.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        emails = get_emails_from_database()
        subject = request.form.get('subject') 
        body = request.form.get('body')  

        attachments = request.files.getlist('attachment')
        
        if attachments:
            msg = Message(subject, recipients=[email])
            msg.body = body

            total_attachments_size = 0  # Inicializa la variable para el tamaño total

            # Adjuntar todos los archivos al mensaje
            for file in attachments:
                if file.filename:
                    filename = file.filename
                    filesize = file.__sizeof__
                    upload_path = Path(__file__).parent / 'uploads' / filename
                    print(filesize) 
                    file.save(upload_path)
                    with open(upload_path, 'rb') as fp:
                        msg.attach(filename, 'application/octet-stream', fp.read())
            
                    total_attachments_size += Path(upload_path).stat().st_size  # Suma el tamaño del archivo
                    print('El tamaño de los archivos es', total_attachments_size)

                    if total_attachments_size > 10 * 1024 * 1024:  # 10 MB en bytes
                        return 'El tamaño total de los archivos adjuntos excede el límite de 10 MB'

            # Enviar el mensaje con todos los archivos adjuntos
            mail.send(msg)

            # Elimina los archivos adjuntos después de enviar el correo
            for file in attachments:
                if file.filename:
                    upload_path = Path(__file__).parent / 'uploads' / file.filename
                    upload_path.unlink()  # Elimina el archivo

            sent_successfully = True

            return render_template('index.html', emails=emails, sent_successfully=sent_successfully)

        else:

            return 'No se han adjuntado archivos'

    emails = get_emails_from_database()

    return render_template('index.html', emails=emails)

