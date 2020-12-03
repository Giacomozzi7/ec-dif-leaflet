import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__,template_folder='plantillas')
from pymongo import MongoClient
from query import buscarId

#Buscador de ID
@app.route('/',methods=["GET"])
def index():  #Se define la ruta del Web Server
    return render_template("index.html")


@app.route("/resultado", methods=["POST"])

def buscaData():
    req = request.form
    sId = str(req['id'])
    sLat = str(req['lat'])
    sLon = str(req['lon'])

    aCoord,aInput,nVel,nSat = buscarId(sId,sLat,sLon)

    if len(aCoord)>0:
        return render_template("resultado.html",Get_id = sId,Get_coord =aCoord, Get_vel = nVel, Get_input=aInput, Get_sat=nSat)
    else:
        return "ID no encontrado"


if __name__ == "__main__":
    app.run()