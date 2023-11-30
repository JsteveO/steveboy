from flask import Flask, request, send_file, render_template   #, session
import sett 
import dict
import services
import pandas as pd




app = Flask(__name__, template_folder='templates')
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SECRET_KEY'] = 'secreto'
#Session(app)

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        
        services.administrar_chatbot(text, number,messageId,name)
        return text

    except Exception as e:
        return 'no enviado ' + str(e)

@app.route('/descargar_csv')
def descargar_csv():
    return send_file('clientes.csv', as_attachment=True, download_name='clientes.csv')

      
@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    #'<h1 style="text-align: center; color: red;">Hola mundo desde glitch, ya no me quiero morir este es mi personal Project</h1>'
    #filtro = session.get('data', None)
    
    if sett.sets is None:
        return '''     
        <html>
            <body>
                <h1 style="text-align: center; color: blue;">
                    Hella world desde mi Personal Project, 😎 .
                </h1>
                <div style="text-align: center;">
                    <img src="https://media.tenor.com/rFe-MW03t1EAAAAC/unicorn-rainbow.gif" alt="La burla" style="display: block; margin: auto;">
                </div>
            </body>
        </html>
        '''
      
    df_html = sett.sets.to_html(classes='table table-bordered styled-table', index=False, escape=False)
    sett.sets.to_csv('clientes.csv', index=False)
    #df_html2 = sett.sets.to_html()
    
    return render_template('bienvenido.html', df_html=df_html)
    #send_file('clientes.csv', as_attachment=True, download_name='clientes.csv')
      

if __name__ == '__main__':
    app.run(debug=True)
