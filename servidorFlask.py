# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 15:33:32 2021

@author: Cristian
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask
from flask import request
import os
from twilio.rest import Client

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/email")
def enviarCorreo():
    hashString = request.args.get("hash")
    print(hashString)
    if(hashString == os.environ.get('SECURITY_HASH')):
        
        destino = request.args.get("email")
        asunto = request.args.get("asunto")
        mensaje = request.args.get("mensaje")
        message = Mail(
        from_email='halfonsom326@gmail.com',
        to_emails=destino,
        subject=asunto,
        html_content=mensaje)        
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print("Enviado")
            return "OK"
        except Exception as e:
            print(e.message)
            return "KO";
    else:
        print("Sin hash")
        return "hash error"

        
@app.route("/sms")
def enviarSms():
    hashString = request.args.get("hash")
    if(hashString == os.environ.get('SECURITY_HASH')):
        destino = request.args.get("destino")
        mensaje = request.args.get("mensaje")
        try:
            account_sid = os.environ["TWILIO_ACCOUNT_SID"]
            auth_token = os.environ["TWILIO_AUTH_TOKEN"]
            client = Client(account_sid, auth_token)
            
            message = client.messages \
                            .create(
                                 body=mensaje,
                                 from_="+12053080705",
                                 to="+57"+destino
                             )
            
            print(message.sid)
            print("Enviado")
            return "OK"
        except Exception as e:
            print(e.message)
            return "KO";
    else:
        print("Sin hash")
        return "hash error"

if __name__=='__main__':
    app.run()