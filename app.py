import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__,template_folder='plantillas')
from pymongo import MongoClient
from query import buscarId
import sympy as sp

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

@app.route('/form',methods=["GET"])
def form():  #Se define la ruta del Web Server
    return render_template("form.html")

@app.route("/ptomedio", methods=["POST"])
def ResolvEc():
    aRes=[]
    req = request.form
    sFuncion = str(req['funcion'])
    sW = str(req['w'])
    sT= str(req['t'])
    sMax= str(req['max'])
    sH = str(req['h'])
    sI = str(req['i'])

    try:
        nW = int(sW);nT = int(sT);nMax = int(sMax)
        nH = int(sH);nI = int(sI)
        f = sp.sympify(sFuncion)

        while nT<nMax:
            nI=nI+1
            ftw=f.evalf(subs={'x':nT})
            ftw=ftw.evalf(subs={'y':nW})

            F = f.evalf(subs={'x':nT+nH/2})
            F = f.evalf(subs={'y':nW+ftw*nH/2})

            nW= nW+F*nH
            nT+=nH

            aRes.append([nI,nT,nW]) 
        print(aRes)

        aParams=[sFuncion,sW,sT,sMax,sH,sI]
        return render_template("ptomedio.html",aRes = aRes, aParams=aParams)

    except:
        return "Valores ingresados inválidos"


if __name__ == "__main__":
    app.run()