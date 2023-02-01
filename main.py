import smtplib, ssl
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, session, url_for
from google.cloud import firestore
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin, login_manager
from secret import secret, secret_key,usersdb,usersdbadm
import json
import bottleneck as bn
import os
from email.message import EmailMessage
import ssl
import smtplib
import time
from base64 import b64decode
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self,username):
        super().__init__()
        self.id= username
        self.username = username
        self.par = {}

    def id(username):
            id= list(logincred.values()).index(username)
            print(id)
            return id

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/login1.html'

@login.user_loader
def load_user(username):
    if username in logincred:
        return User(username)
    return None

@app.route('/pag1')
def root():
    if 'loggedin' not in session or session["loggedin"]==False:
        return redirect('/static/login1.html')
    else:
        return redirect('/static/registraovisualizza.html')

@app.route('/', methods=['GET'])
def main():
    return redirect('/static/login1.html')

@login_required
def iduser():
    id_user = User.id(current_user.username)
    id_user = str(id_user)
    return id_user


@app.route('/graph/sensor1', methods=['GET'])
@login_required
def nome():
    global nome
    nome = User.id(current_user.username)
    nome = str(nome)
    return redirect('/graph/sensor1/'+nome)

@app.route('/graph2/sensor2', methods=['GET'])
@login_required
def nome2():
    global nome2
    nome = User.id(current_user.username)
    nome=str(nome)
    return redirect('/graph2/sensor2/'+nome)

@app.route('/graph3/sensor3', methods=['GET'])
@login_required
def nome3():
    nome = User.id(current_user.username)
    nome=str(nome)
    return redirect('/graph3/sensor3/'+nome)

@app.route('/graph4/sensor4', methods=['GET'])
@login_required
def nome4():
    nome = User.id(current_user.username)
    nome=str(nome)
    return redirect('/graph4/sensor4/'+nome)

@app.route('/graph5/sensor5', methods=['GET'])
@login_required
def nome5():
    nome = User.id(current_user.username)
    nome=str(nome)
    return redirect('/graph5/sensor5/'+nome)

@app.route('/graph6/sensor6', methods=['GET'])
@login_required
def nome6():
    nome = User.id(current_user.username)
    nome=str(nome)
    return redirect('/graph6/sensor6/'+nome)

@app.route('/sensors/sensor1/<nome>', methods=['GET'])
def read_all(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    acc = []
    for doc in db.collection('Accelerometer'+nome).stream():
        x = doc.to_dict()
        acc.append([x['tempo'+nome].split(" ")[0], float(x['ax'+nome]), float(x['ay'+nome]), float(x['az'+nome])])
    sogliaacc(-0.53125,0.375,0.734375, nome)
    print(sogliaacc(-0.53125,0.375,0.734375, nome)[1])
    if sogliaacc(-0.53125,0.375,0.734375, nome)[0] < -0.53125:
            alert(-0.53125, "ACCELERATION ALONG EACH AXIS")
    if (sogliaacc(-0.53125,0.375,0.734375, nome)[1]) > 0.375:
            alert(0.375, "ACCELERATION ALONG EACH AXIS")
    if sogliaacc(-0.53125,0.375,0.734375, nome)[2] > 0.734375:
            alert(0.734375, "ACCELERATION ALONG EACH AXIS")
    return json.dumps(acc)

@app.route('/sensors/sensor2/<nome>', methods=['GET'])
@login_required
def read_all2(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    bvp = []
    for doc in db.collection('Blood Volume Pulse'+nome).stream():
        x = doc.to_dict()
        bvp.append([x['tempo'+nome], float(x['bvp'+nome])])
    sogliabvp(8, nome)
    if sogliabvp(8, nome) > 8:
        alert(8, "BLOOD VOLUME PULSE")
    return json.dumps(bvp)

@app.route('/sensors/sensor3/<nome>', methods=['GET'])
def read_all3(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    eda = []
    for doc in db.collection('Electrodermal activity'+nome).stream():
        x = doc.to_dict()
        eda.append([x['tempo'+nome], float(x['eda'+nome])])
    sogliaeda(0.744, nome)
    if sogliaeda(0.744, nome) > 0.744:
        alert(0.744, "ELECTRODERMAL ACTIVITY")
    return json.dumps(eda)


@app.route('/sensors/sensor4/<nome>', methods=['GET'])
def read_all4(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    hr = []
    for doc in db.collection('Average heart rate'+nome).stream():
        x = doc.to_dict()
        hr.append([x['tempo'+nome], float(x['hr'+nome])])
    sogliahr(90, nome)
    if sogliahr(90, nome) > 90:
        alert(90, "AVERAGE HEART RATE")
    return json.dumps(hr)

@app.route('/sensors/sensor5/<nome>', methods=['GET'])
def read_all5(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    ibi = []
    for doc in db.collection('Time between individuals heart'+nome).stream():
        x = doc.to_dict()
        ibi.append([x['tempo'+nome], float(x['ibi'+nome])])
    sogliaibi(844.92, nome)
    if sogliaibi(844.92, nome) > 844.92:
        alert(844.92, "TIME BETWEEN INDIVIDUALS HEART")
    return json.dumps(ibi)

@app.route('/sensors/sensor6/<nome>', methods=['GET'])
def read_all6(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    skin_temperature = []
    for doc in db.collection('Data from temperature sensor'+nome).stream():
        x = doc.to_dict()
        skin_temperature.append([x['tempo'+nome], float(x['skin_temperature'+nome])])
    sogliaskintemperature(34.6, nome)
    if sogliaskintemperature(34.6, nome) > 34.6:
        alert(34.6, "DATA FROM TEMPERATURE SENSOR")
    return json.dumps(skin_temperature)

@app.route('/sensor1/parameter/<nome>', methods=['POST'])
def rollavg_bottleneck(a,n,nome):
    return bn.move_mean(a, window=3, min_count=None)

def media_mobile(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    vecx= []
    vecy=[]
    vecz=[]
    meanx = 0
    meany = 0
    meanz = 0
    for doc in db.collection('Accelerometer'+nome).stream():
        x = doc.to_dict()
        vecx.append(float(x['ax'+nome]))
        vecy.append(float(x['ay' + nome]))
        vecz.append(float(x['az' + nome]))
        if len(vecx)>3:
            vecx = vecx[-3:]
            meanx = rollavg_bottleneck(vecx,3,nome)
            meanx = meanx[-1:]
        if len(vecy)>3:
            vecy = vecy[-3:]
            meany = rollavg_bottleneck(vecy,3,nome)
            meany = meany[-1:]
        if len(vecz)>3:
            vecz = vecz[-3:]
            meanz = rollavg_bottleneck(vecz,3,nome)
            meanz = meanz[-1:]
    return meanx,meany,meanz


def media_mobile_bvp(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    vecbvp= []
    meanbvp = 0
    for doc in db.collection('Blood Volume Pulse'+nome).stream():
        x = doc.to_dict()
        vecbvp.append(float(x['bvp'+nome]))
        if len(vecbvp)>3:
            vecbvp = vecbvp[-3:]
            meanbvp = rollavg_bottleneck(vecbvp,3,nome)
            meanbvp = meanbvp[-1:]
    return meanbvp

def media_mobile_eda(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    veceda= []
    meaneda = 0
    for doc in db.collection('Electrodermal activity'+nome).stream():
        x = doc.to_dict()
        veceda.append(float(x['eda'+nome]))
        if len(veceda)>3:
            veceda = veceda[-3:]
            meaneda = rollavg_bottleneck(veceda,3,nome)
            meaneda = meaneda[-1:]
    return meaneda

def media_mobile_hr(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    vechr= []
    meanhr = 0
    for doc in db.collection('Average heart rate'+nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        vechr.append(float(x['hr'+nome]))
        if len(vechr)>3:
            vechr = vechr[-3:]
            meanhr = rollavg_bottleneck(vechr,3,nome)
            meanhr = meanhr[-1:]
    return meanhr

def media_mobile_ibi(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    vecibi= []
    meanibi = 0
    for doc in db.collection('Time between individuals heart'+nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        vecibi.append(float(x['ibi'+nome]))
        if len(vecibi)>3:
            vecibi = vecibi[-3:]
            meanibi = rollavg_bottleneck(vecibi,3,nome)
            meanibi = meanibi[-1:]
    return meanibi

def media_mobile_skin_temperature(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    vec_skin_temperature= []
    mean_skin_temperature = 0
    for doc in db.collection('Data from temperature sensor'+nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        vec_skin_temperature.append(float(x['skin_temperature'+nome]))
        if len(vec_skin_temperature)>3:
            vec_skin_temperature = vec_skin_temperature[-3:]
            mean_skin_temperature = rollavg_bottleneck(vec_skin_temperature,3,nome)
            mean_skin_temperature = mean_skin_temperature[-1:]
    return mean_skin_temperature

def mediabvp(nome):
        db = firestore.Client.from_service_account_json('credentials.json')
        m = []
        media=0
        for doc in db.collection('Blood Volume Pulse'+nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
            x = doc.to_dict()  # ottengo un dizionario dal documento
            m.append(float(x['bvp'+nome]))
            somma = 0
            for j in range(len(m)):
                somma += m[j]
                media = somma / len(m)
                media= round(media,2)
        return json.dumps(media)

def mediaeda(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    m = []
    media=0
    for doc in db.collection('Electrodermal activity' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        m.append(float(x['eda' + nome]))
        somma = 0
        for j in range(len(m)):
            somma += m[j]
            media = somma / len(m)
            media = round(media, 2)
    return json.dumps(media)

def mediahr(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    m = []
    media=0
    for doc in db.collection('Average heart rate' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        m.append(float(x['hr' + nome]))
        somma = 0
        for j in range(len(m)):
            somma += m[j]
            media = somma / len(m)
            media = round(media, 2)
    return json.dumps(media)

def mediaibi(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    m = []
    media=0
    for doc in db.collection('Time between individuals heart' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        m.append(float(x['ibi' + nome]))
        somma = 0
        for j in range(len(m)):
            somma += m[j]
            media = somma / len(m)
            media = round(media, 2)
    return json.dumps(media)

def media_skin_temperature(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    m = []
    media=0
    for doc in db.collection('Data from temperature sensor' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        m.append(float(x['skin_temperature' + nome]))
        somma = 0
        for j in range(len(m)):
            somma += m[j]
            media = somma / len(m)
            media = round(media, 2)
    return json.dumps(media)

def minimobvp(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    minbvp = []
    minimo=0
    for doc in db.collection('Blood Volume Pulse'+ nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        minbvp.append(float(x['bvp' + nome]))
        minimo=min(minbvp)
    return minimo

def minimoeda(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    mineda = []
    minimo=0
    for doc in db.collection('Electrodermal activity'+ nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        mineda.append(float(x['eda' + nome]))
        minimo=min(mineda)
    return minimo

def minimohr(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    minhr = []
    minimo=0
    for doc in db.collection('Average heart rate'+ nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        minhr.append(float(x['hr' + nome]))
        minimo=min(minhr)
    return minimo

def minimoibi(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    minibi = []
    minimo=0
    for doc in db.collection('Time between individuals heart'+ nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        minibi.append(float(x['ibi' + nome]))
        minimo=min(minibi)
    return minimo

def minimo_skin_temperature(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    min_skin_temperature= []
    minimo=0
    for doc in db.collection('Data from temperature sensor'+ nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        min_skin_temperature.append(float(x['skin_temperature' + nome]))
        minimo=min(min_skin_temperature)
    return minimo

def massimobvp(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    maxbvp = []
    massimo=0
    for doc in db.collection('Blood Volume Pulse' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        maxbvp.append(float(x['bvp' + nome]))
        massimo=max(maxbvp)
    return massimo

def massimoeda(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    maxeda = []
    massimo=0
    for doc in db.collection('Electrodermal activity' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        maxeda.append(float(x['eda' + nome]))
        massimo=max(maxeda)
    return massimo

def massimoibi(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    maxibi = []
    massimo=0
    for doc in db.collection('Time between individuals heart' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        maxibi.append(float(x['ibi' + nome]))
        massimo=max(maxibi)
    return massimo

def massimohr(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    maxhr = []
    massimo=0
    for doc in db.collection('Average heart rate' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        maxhr.append(float(x['hr' + nome]))
        massimo=max(maxhr)
    return massimo

def massimo_skin_temperature(nome):
    db = firestore.Client.from_service_account_json('credentials.json')
    max_skin_temperature = []
    massimo=0
    for doc in db.collection('Data from temperature sensor' + nome).stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
        x = doc.to_dict()  # ottengo un dizionario dal documento
        max_skin_temperature.append(float(x['skin_temperature' + nome]))
        massimo=max(max_skin_temperature)
    return massimo

def alert(s,grafico):
    from app_password import password
    email_sender = 'davideficarelli46@gmail.com'
    email_password = password
    email_receiver = current_user.username+"@gmail.com"
    subject = "ALERT:"+ str(grafico)
    body = "Ciao, " + current_user.username + "\n Attenzione! È stata rilveta un'anomalia: Hai superato il valore soglia di "+str(s)+" \nVisita il sito http://127.0.0.1:8080 per maggiori informazioni."
    e_m = EmailMessage()
    e_m['From'] = email_sender
    e_m['To'] = email_receiver
    e_m['Subject'] = subject
    e_m.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, e_m.as_string())

def sogliaacc(sx,sy,sz,nome):
    mediamx = []
    mediamy = []
    mediamz = []
    maxx = 0
    maxy = 0
    maxz = 0
    mediamx.insert(0,media_mobile(nome)[0])
    mediamy.insert(0,media_mobile(nome)[1])
    mediamz.insert(0,media_mobile(nome)[2])
    for i in range(len(mediamx)):
        if (float(mediamx[i])) > sx:
            maxx = mediamx[i]
    for j in range(len(mediamy)):
        if (float(mediamy[j])) > sy:
            maxy = mediamy[j]
    for k in range(len(mediamz)):
        if (float(mediamz[k])) > sz:
            maxz = mediamz[k]
    return round(float(maxx),2),round(float(maxy),2),round(float(maxz),2)


def sogliabvp(s,nome):
    mediambvp = []
    max = 0
    mediambvp.insert(0,media_mobile_bvp(nome))
    for j in range(len(mediambvp)):
        if float(mediambvp[j]) > s:
            max = mediambvp[j]
    return float(max)

def sogliaeda(s, nome):
    mediameda = []
    max = 0
    mediameda.insert(0, media_mobile_eda(nome))
    for j in range(len(mediameda)):
        if float(mediameda[j]) > s:
            max = mediameda[j]
    return float(max)

def sogliahr(s, nome):
    mediamhr = []
    max = 0
    mediamhr.insert(0, media_mobile_hr(nome))
    for j in range(len(mediamhr)):
        if float(mediamhr[j]) > s:
            max = mediamhr[j]
    return float(max)

def sogliaibi(s, nome):
    mediamibi = []
    max = 0
    mediamibi.insert(0, media_mobile_ibi(nome))
    for j in range(len(mediamibi)):
        if float(mediamibi[j]) > s:
            max = mediamibi[j]
    return float(max)

def sogliaskintemperature(s, nome):
    mediam_skin_temperature = []
    max = 0
    mediam_skin_temperature.insert(0, media_mobile_skin_temperature(nome))
    for j in range(len(mediam_skin_temperature)):
        if float(mediam_skin_temperature[j]) > s:
            max = mediam_skin_temperature[j]
    return float(max)

@app.route('/graph/sensor1/<nome>', methods=['GET'])
@login_required
def graph(nome):
        acc = json.loads(read_all(nome))
        acc.insert(0, ['tempo', 'ax','ay','az'])
        if sogliaacc(-0.53125,0.375,0.734375,nome)>(0,0,0):
            return render_template('graficoacc.html', acc=acc, sogliaacc=(sogliaacc(-0.53125,0.375,0.734375,nome)))
        else:
            return render_template('graficoacc2.html', acc=acc)

@app.route('/graph2/sensor2/<nome>', methods=['GET'])
@login_required
def graph2(nome):
    bvp = json.loads(read_all2(nome))
    bvp.insert(0, ['tempo', 'bvp'])
    sogliabvp(8,nome)
    if sogliabvp(8,nome)>0:
        return render_template('graficobvp.html', bvp=bvp, sogliabvp=sogliabvp(6,nome), mediabvp=mediabvp(nome), minimobvp=minimobvp(nome), massimobvp=massimobvp(nome))
    else:
        return render_template('graficobvp2.html', bvp=bvp, mediabvp=mediabvp(nome),minimobvp=minimobvp(nome), massimobvp=massimobvp(nome))

@app.route('/graph3/sensor3/<nome>', methods=['GET'])
@login_required
def graph3(nome):
    eda = json.loads(read_all3(nome))
    eda.insert(0, ['tempo', 'eda'])
    sogliaeda(0.744, nome)
    if sogliaeda(0.744, nome) > 0:
        return render_template('graficoeda.html', eda=eda, sogliaeda=sogliaeda(0.744, nome), mediaeda=mediaeda(nome),
                               minimoeda=minimoeda(nome), massimoeda=massimoeda(nome))
    else:
        return render_template('graficoeda2.html', eda=eda, mediaeda=mediaeda(nome), minimoeda=minimoeda(nome),
                               massimoeda=massimoeda(nome))

@app.route('/graph4/sensor4/<nome>', methods=['GET'])
@login_required
def graph4(nome):
    hr = json.loads(read_all4(nome))
    hr.insert(0, ['tempo', 'hr'])
    sogliahr(90, nome)
    if sogliahr(90, nome) > 0:
        return render_template('graficohr.html', hr=hr, sogliahr=(sogliahr(90,nome)), mediahr=mediahr(nome),
                               minimohr=minimohr(nome), massimohr=massimohr(nome))
    else:
        return render_template('graficohr2.html', hr=hr, mediahr=mediahr(nome), minimohr=minimohr(nome),
                               massimohr=massimohr(nome))

@app.route('/graph5/sensor5/<nome>', methods=['GET'])
@login_required
def graph5(nome):
    ibi = json.loads(read_all5(nome))
    ibi.insert(0, ['tempo', 'ibi'])
    sogliaibi(844.92, nome)
    if sogliahr(844.92, nome) > 0:
        return render_template('graficoibi.html', ibi=ibi, sogliaibi=(sogliaibi(844.92,nome)), mediaibi=mediaibi(nome),
                               minimoibi=minimoibi(nome), massimoibi=massimoibi(nome))
    else:
        return render_template('graficoibi2.html', ibi=ibi, mediaibi=mediaibi(nome), minimoibi=minimoibi(nome),
                               massimoibi=massimoibi(nome))

@app.route('/graph6/sensor6/<nome>', methods=['GET'])
@login_required
def graph6(nome):
    skin_temperature = json.loads(read_all6(nome))
    skin_temperature.insert(0, ['tempo', 'skin_temperature'])
    sogliaskintemperature(34.6, nome)
    if sogliaskintemperature(34.6, nome) > 0:
        return render_template('graficoskintemperature.html', skin_temperature=skin_temperature,
                               sogliaskintemperature=(sogliaskintemperature(34.6,nome)),
                               media_skin_temperature=media_skin_temperature(nome),
                               minimo_skin_temperature=minimo_skin_temperature(nome),
                               massimo_skin_temperature=massimo_skin_temperature(nome))
    else:
        return render_template('graficoskintemperature2.html', skin_temperature=skin_temperature,
                               media_skin_temperature=media_skin_temperature(nome),
                               minimo_skin_temperature=minimo_skin_temperature(nome),
                               massimo_skin_temperature=massimo_skin_temperature(nome))


@app.route('/sensors/sensor1/<nome>', methods=['POST'])
def save_data(nome):

        tempo = request.values['tempo'+nome]
        ax = request.values["ax"+nome]
        ay = request.values['ay'+nome]
        az = request.values['az'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Accelerometer'+nome).document(tempo).set({'tempo'+nome: tempo, 'ax'+nome: ax, 'ay'+nome: ay, 'az'+nome: az})

        return 'ok', 200

@app.route('/sensors/sensor2/<nome>', methods=['POST'])
def save_data2(nome):

        tempo = request.values['tempo'+nome]
        bvp = request.values['bvp'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Blood Volume Pulse'+nome).document(tempo).set({'tempo'+nome: tempo, 'bvp'+nome: bvp})
        return 'ok', 200

@app.route('/sensors/sensor3/<nome>', methods=['POST'])
def save_data3(nome):
        tempo = request.values['tempo'+nome]
        eda = request.values['eda'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Electrodermal activity'+nome).document(tempo).set({'tempo'+nome: tempo, 'eda'+nome: eda})
        return 'ok', 200

@app.route('/sensors/sensor4/<nome>', methods=['POST'])
def save_data4(nome):
        tempo = request.values['tempo'+nome]
        hr = request.values['hr'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Average heart rate'+nome).document(tempo).set({'tempo'+nome: tempo, 'hr'+nome: hr})
        return 'ok', 200

@app.route('/sensors/sensor5/<nome>', methods=['POST'])
def save_data5(nome):
        tempo = request.values['tempo'+nome]
        ibi = request.values['ibi'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Time between individuals heart'+nome).document(tempo).set({'tempo'+nome: tempo, 'ibi'+nome: ibi})
        return 'ok', 200

@app.route('/sensors/sensor6/<nome>', methods=['POST'])
def save_data6(nome):
        tempo = request.values['tempo'+nome]
        skin_temperature = request.values['skin_temperature'+nome]
        db = firestore.Client.from_service_account_json('credentials.json')
        db.collection('Data from temperature sensor'+nome).document(tempo).set({'tempo'+nome: tempo, 'skin_temperature'+nome: skin_temperature})
        return 'ok', 200

@app.route('/register', methods=['POST'])
def register():
    global logincred
    username=request.form['u']
    password=request.form['p']
    usersdb[username] = password
    db = firestore.Client.from_service_account_json('credentials.json')
    db.collection('usersdb').document().set({'username': username, 'password': password, 'create_time': firestore.SERVER_TIMESTAMP})
    db = firestore.Client.from_service_account_json('credentials.json')
    logincred = {}
    for doc in db.collection('usersdb').order_by('create_time').stream():
        x = doc.to_dict()  #
        logincred[x['username']] = x['password']
    return redirect('/static/login1.html')

db = firestore.Client.from_service_account_json('credentials.json')
logincred = {}
for doc in db.collection('usersdb').order_by('create_time').stream():  # abbiamo i documenti e vogliamo accedere ai campi del documento
    x = doc.to_dict()  # ottengo un dizionario dal documento
    logincred[x['username']]=x['password']
    print(logincred)

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.values['u']
    password = request.values['p']
    if username in logincred and password==logincred[username]:
        login_user(User(username), remember=True)
        session["loggedin"] = True
        session["nome"] = username
        return redirect('/static/visualizzaGrafici.html')
    else:
        return redirect('/static/login1.html')

@app.route('/loginadmin', methods=['POST'])
def loginadmin():
    username = request.values['u']
    password = request.values['p']
    if username in usersdbadm and usersdbadm[username] == password:
        session["loggedin"] = True
        session["nome"] = username
        return redirect('/pag1')
    else:
        return redirect('/static/login1.html')

@app.route('/logout')
def logout():
        session.pop('username', None)
        return redirect('/static/login1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)