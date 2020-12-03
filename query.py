from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost'

client =MongoClient(MONGO_URI)

db = client['datos']
coleccion =db['data']

def buscarId(sId,sLat,sLon):
    aCoord=[]; aQuery=[]; aInput=[];nVel=0;nSat=0
    #Se establece el dato que se desea agrupar
    try: sId=int(sId)
    except: pass
    dictGroup = { "$group": {
                    "_id": "$_id",
                    "lat": { "$push": "$lat" },
                    "lon": { "$push": "$lon" },
                    "fecha": { "$push": "$fecha" },
                    "vel": { "$push": "$vel" },
                    "nsat": { "$push": "$nsat" },
                }}

    # ORDER BY : fecha ASC
    dictSort = {'$sort' : { 'fecha': 1 }}

    #Match con el Id
    dictMatch={"$match": { "id":{ "$eq":sId}}}

    aQuery.append(dictMatch);aQuery.append(dictGroup);aQuery.append(dictSort)

    #Obtiene latitud y longitud para el id ingresado
    b = db.data.aggregate(aQuery)
    for i in b:
        aCoord.append([i["lat"][0],i["lon"][0]])
        print(i["lat"][0],i["lon"][0])

        #Si las coordenadas ingresadas por pantalla estan en los registros del vehiculo 
        #Se guardan las coordenadas, velocidad y n satelites
        if str(i["lat"][0])==sLat and str(i["lon"][0])==sLon: 
            aInput=[i["lat"][0],i["lon"][0]]
            nVel = i["vel"][0]
            nSat = i["nsat"][0]


    return aCoord,aInput,nVel,nSat
