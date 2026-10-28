from fastapi import FastAPI
import sqlite3

app=FastAPI()

#conexion db
def conectardb():
    return sqlite3.connect("DB_Hotel.db")


#iniciar
@app.get("/")
def inicio():
    return{"sistema para reservar el hotel"}

#Hoteles 
@app.get("/hoteles")
def hoteles():
    conexion=conectardb()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FORM hoteles")
    datos = cursor.fetchall()

    conexion.close()
    return datos

# hab disponibles

@app.get ("/disponibilidad")
def disponibilidad(hotel_id: int, tipo: str, fecha_inicio: str, fecha_fin:str):
    conexion:conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM habitaciones
        WHERE hotel_id = ?
        AND TIPO = ?
        AND id NOT IN (
        SELECT habitacion_id FROM reservas 
        AND fecha_fin > ? 
        )
        """, (hotel_id, tipo, fecha_fina, fecha_inicio))

    datos=cursor.fetchall()
    conexion.close()

    return{"habitacion_disponible":len(datos), "habitaciones": datos }

#Tarifas

@app.get("/tarigfas")
def trafifas(hotel_id:int, tipo:str, temporada:str, personas:int):

     cursor.execute("""
            SELECT * FROM tarifas
            WHERE hotel_id = ?
            AND tipo =?
            AND temporada=?

            AND personas =?
            )
            """, (hotel_id, tipo, temporada, personas))


     dato=cursor.fetchone()
     conexion.close()


     if dato: 
         return {"precio por noche":dato[0]}
     else:
         return{"tarifa no encontrada"}

# cotizacion 

from datetime import date

@app.get("/cotizar")
def cotizar (hotel_id: int, tipo: str, temporada:str, personas: int, habitaciones: int, fecha_inicio: str, fecha_fin: str):
    try:
        noches = (date.fromisoformat(fecha_fin)-date(fromisformat(fecha_inicio))).days
    except ValueError:
        return{"fechas incorrectas"}

    if noches <= 0 or personas <1 or habitaciones < 1: 
        return {"error de datos"}


    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute( "SELECT capacidad FROM hoteles WHERE id = ?", (hotel_id,))

    hotel = cursor.fetchone()

    if not hotel or personas < habitaciones or personas > habitaciones * hotel[0]:
        conexion.close()
        return {"error": "Capacidad incorrecta"}

    cursor.execute("""
        SELECT COUNT(*) FROM habitaciones
        WHERE hotel_id = ? AND tipo = ?
        AND id NOT IN (
        SELECT habitacion_id FROM reservas
        WHERE fecha_inicio < ? AND fecha_fin > ?
        )""", (hotel_id, tipo, fecha_fin, fecha_inicio))
    

    disponibles = cursor.fetchone()[0]

    if disponibles < habitaciones:
        conexion.close()
        return {"error": "No hay disponibilidad"}

    total = 0
    for i in range(habitaciones):
        ocupacion = personas // habitaciones

        if i < personas % habitaciones:

            ocupacion += 1

        cursor.execute("""
            SELECT precio FROM tarifas
            WHERE hotel_id = ? AND tipo = ?
            AND temporada = ? AND personas = ?
        """, (hotel_id, tipo, temporada, ocupacion))

        tarifa = cursor.fetchone()
        if not tarifa:
            conexion.close()
            return {"error": "Tarifa no encontrada"}

        total += tarifa[0] * noches

    conexion.close()

    return {"noches": noches, "total": total}






    