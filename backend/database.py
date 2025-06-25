import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# --- Configuración de Conexión ---
# Idealmente, esto debería venir de un archivo .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "sistema_ventas")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# --- Colecciones ---
vendedores_collection = db["vendedores"]
ventas_collection = db["ventas"]
reglas_collection = db["reglas"]
historial_collection = db["historial"]

def seed_database():
    """
    Solo inserta los datos de ejemplo si las colecciones están vacías.
    No borra datos existentes.
    """
    print("--- VERIFICANDO SI ES NECESARIO PLANTAR DATOS DE EJEMPLO ---")
    # 1. Insertar datos de Vendedores si está vacío
    if vendedores_collection.count_documents({}) == 0:
        print("Poblando la colección de vendedores...")
        vendedores_collection.insert_many([
            {"_id": 1, "nombre": "Perico", "email": "perico@empresa.com"},
            {"_id": 2, "nombre": "Sola", "email": "sola@empresa.com"},
            {"_id": 3, "nombre": "Carlos", "email": "carlos@empresa.com"},
            {"_id": 4, "nombre": "María", "email": "maria@empresa.com"}
        ])
    # 2. Insertar datos de Ventas si está vacío
    if ventas_collection.count_documents({}) == 0:
        print("Poblando la colección de ventas...")
        ventas = []
        id_counter = 1
        # Ventas de ejemplo para 2024
        ventas += [
            {"_id": id_counter, "vendedor_id": 1, "fecha": "2024-01-10", "monto": 100},
            {"_id": id_counter+1, "vendedor_id": 2, "fecha": "2024-02-15", "monto": 200},
            {"_id": id_counter+2, "vendedor_id": 3, "fecha": "2024-03-20", "monto": 300},
            {"_id": id_counter+3, "vendedor_id": 4, "fecha": "2024-04-25", "monto": 400},
        ]
        id_counter += 4
        # Ventas para cada mes de 2025 hasta agosto para todos los vendedores
        for mes in range(1, 9):  # Enero (1) a Agosto (8)
            for vendedor_id in [1, 2, 3, 4]:
                fecha = f"2025-{mes:02d}-15"
                monto = 100 * vendedor_id + mes * 10  # Monto variable
                ventas.append({
                    "_id": id_counter,
                    "vendedor_id": vendedor_id,
                    "fecha": fecha,
                    "monto": monto
                })
                id_counter += 1
        ventas_collection.insert_many(ventas)
    # 3. Insertar Reglas de Comisión si está vacío
    if reglas_collection.count_documents({}) == 0:
        print("Poblando la colección de reglas de comisión...")
        reglas_collection.insert_many([
            {"_id": 1, "vendedor_id": 1, "porcentaje": 10, "descripcion": "10% para Perico"},
            {"_id": 2, "vendedor_id": 2, "porcentaje": 8, "descripcion": "8% para Sola"},
            {"_id": 3, "vendedor_id": 3, "porcentaje": 12, "descripcion": "12% para Carlos"},
            {"_id": 4, "vendedor_id": 4, "porcentaje": 9, "descripcion": "9% para María"}
        ])
    print("--- DATOS DE EJEMPLO SOLO SE INSERTARON SI LAS COLECCIONES ESTABAN VACÍAS ---")

def object_id_to_str(data):
    """
    Convierte ObjectId a string en documentos y listas de documentos.
    Mantiene los IDs enteros tal cual para relaciones correctas.
    """
    if isinstance(data, list):
        return [object_id_to_str(item) for item in data]
    if isinstance(data, dict):
        if '_id' in data:
            # Si el _id es ObjectId, conviértelo a string, si es int, déjalo igual
            if isinstance(data['_id'], ObjectId):
                data['id'] = str(data['_id'])
            else:
                data['id'] = data['_id']
            del data['_id']
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
    return data 