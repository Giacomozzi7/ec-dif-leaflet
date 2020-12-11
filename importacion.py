#Por Francisco Giacomozzi R.
#----------------------------------------------
import csv
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost'

client =MongoClient(MONGO_URI)

db = client['data']
coleccion =db['datos']
c=0
with open('full.csv', newline='') as BDD:
    reader = csv.reader(BDD)
    for fila in reader:
        dic = {'id':int(fila[0]),'lat':float(fila[1]),'lon':float(fila[2]),'vel':int(fila[3]),
              'ang':int(fila[4]),'fecha':fila[5],'ign':int(fila[6]),'nsat':int(fila[7])}
        c=c+1
        print(c)
        coleccion.insert_one(dic)

