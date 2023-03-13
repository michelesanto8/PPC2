import time

from flask import render_template
from google.cloud import firestore
from datetime import datetime
from requests import get,post
from secret import secret
from main import logincred
#sensore che manda i dati al server
base_url = 'https://pervasiveandcloudcomputing2.oa.r.appspot.com'


for i in range(len(logincred)):
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0'+str(i)+'/wrist_acc.csv') as file1:
                for r in file1:
                    timestamp,ax,ay,az = r.split(';')
                    timestamp = int(timestamp)
                    tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                    r = post(f'{base_url}/sensors/sensor1/'+str(i), data={'tempo'+str(i): tempo, 'ax'+str(i): ax, 'ay'+str(i): ay, 'az'+str(i): az, 'secret': secret})
                    print('sending',str(i),tempo,ax,ay,az)
                    time.sleep(5)
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0'+str(i)+'/wrist_bvp.csv', encoding='utf-8-sig') as file2:
            for r in file2:
                timestamp,bvp = r.split(';')
                timestamp = int(timestamp)
                tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                r = post(f'{base_url}/sensors/sensor2/'+str(i), data={'tempo'+str(i): tempo, 'bvp'+str(i): bvp, 'secret': secret})
                print('sending',i, tempo, bvp)
                time.sleep(5)
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0' + str(i) + '/wrist_eda.csv', encoding='utf-8-sig') as file3:
            for r in file3:
                timestamp, eda = r.split(';')
                timestamp = int(timestamp)
                tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                r = post(f'{base_url}/sensors/sensor3/' + str(i),data={'tempo' + str(i): tempo, 'eda' + str(i): eda, 'secret': secret})
                print('sending', i, tempo, eda)
                time.sleep(5)
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0' + str(i) + '/wrist_hr.csv', encoding='utf-8-sig') as file4:
            for r in file4:
                timestamp, hr = r.split(';')
                timestamp = int(timestamp)
                tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                r = post(f'{base_url}/sensors/sensor4/' + str(i),data={'tempo' + str(i): tempo, 'hr' + str(i): hr, 'secret': secret})
                print('sending', i, tempo, hr)
                time.sleep(5)
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0' + str(i) + '/wrist_ibi.csv', encoding='utf-8-sig') as file5:
            for r in file5:
                timestamp, ibi = r.split(';')
                timestamp = int(timestamp)
                tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                r = post(f'{base_url}/sensors/sensor5/' + str(i),data={'tempo' + str(i): tempo, 'ibi' + str(i): ibi, 'secret': secret})
                print('sending', i, tempo, ibi)
                time.sleep(5)
        with open('/Users/michelesanto/Desktop/Mamei/Dataset/01/0' + str(i) + '/wrist_skin_temperature.csv', encoding='utf-8-sig') as file6:
            for r in file6:
                timestamp, skin_temperature = r.split(';')
                timestamp = int(timestamp)
                tempo = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S:%-S")
                r = post(f'{base_url}/sensors/sensor6/' + str(i),data={'tempo' + str(i): tempo, 'skin_temperature' + str(i): skin_temperature, 'secret': secret})
                print('sending', i, tempo, skin_temperature)
                time.sleep(5)
