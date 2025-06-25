from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from bson.objectid import ObjectId
from database import (
    vendedores_collection,
    ventas_collection,
    reglas_collection,
    historial_collection,
    seed_database,
    object_id_to_str
)

app = Flask(__name__)
CORS(app)

# Al iniciar la app, se puebla la DB si es necesario
with app.app_context():
    seed_database()

@app.route('/')
def home():
    return jsonify({"message": "Sistema de Comisiones - API con MongoDB funcionando!"})

@app.route('/api/vendedores')
def get_vendedores():
    vendedores = list(vendedores_collection.find())
    return jsonify(object_id_to_str(vendedores))

@app.route('/api/ventas')
def get_ventas():
    ventas = list(ventas_collection.find())
    vendedores = {v['id']: v for v in object_id_to_str(list(vendedores_collection.find()))}
    # Añadir nombre del vendedor a cada venta
    for venta in ventas:
        vendedor_id = venta['vendedor_id']
        venta['vendedor_nombre'] = vendedores.get(vendedor_id, {}).get('nombre', 'Desconocido')
    return jsonify(object_id_to_str(ventas))

@app.route('/api/reglas')
def get_reglas():
    reglas = list(reglas_collection.find())
    return jsonify(object_id_to_str(reglas))

@app.route('/api/historial-comisiones')
def get_historial_comisiones():
    """Obtiene el historial de comisiones con filtros opcionales desde MongoDB."""
    try:
        query = {}
        
        # Filtro por rango de fecha de cálculo
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            query['fecha_calculo'] = {'$gte': fecha_inicio, '$lte': fecha_fin}
        elif fecha_inicio:
            query['fecha_calculo'] = {'$gte': fecha_inicio}
        elif fecha_fin:
            query['fecha_calculo'] = {'$lte': fecha_fin}
            
        # Filtro por vendedor
        vendedor_id = request.args.get('vendedor_id')
        if vendedor_id:
            query['vendedor_id'] = int(vendedor_id)
            
        historial_filtrado = list(historial_collection.find(query))
        
        # Agregar información del vendedor a cada registro
        vendedores = {v['id']: v for v in object_id_to_str(list(vendedores_collection.find()))}
        for registro in historial_filtrado:
            vendedor = vendedores.get(registro['vendedor_id'])
            registro['vendedor_nombre'] = vendedor['nombre'] if vendedor else 'Desconocido'
        
        return jsonify({
            "historial": object_id_to_str(historial_filtrado),
            "total_registros": len(historial_filtrado),
            "total_comisiones": round(sum(r['comision_calculada'] for r in historial_filtrado), 2)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/calcular-comisiones', methods=['POST'])
def calcular_comisiones():
    try:
        data = request.get_json()
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Fechas de inicio y fin son requeridas"}), 400
        resultados = []
        fecha_calculo = datetime.now().strftime('%Y-%m-%d')
        vendedores = list(vendedores_collection.find())
        reglas = list(reglas_collection.find())
        # Convertir fechas a datetime para comparación robusta
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        for vendedor in vendedores:
            vendedor_id = vendedor['_id']
            # Traer todas las ventas del vendedor
            ventas_vendedor_all = list(ventas_collection.find({'vendedor_id': vendedor_id}))
            # Filtrar ventas por fecha usando datetime
            ventas_vendedor = [
                v for v in ventas_vendedor_all
                if 'fecha' in v and fecha_inicio_dt <= datetime.strptime(v['fecha'], '%Y-%m-%d') <= fecha_fin_dt
            ]
            total_ventas = sum(venta['monto'] for venta in ventas_vendedor)
            regla = next((r for r in reglas if r['vendedor_id'] == vendedor_id), None)
            comision = 0
            porcentaje = 0
            if regla:
                porcentaje = regla['porcentaje']
                comision = total_ventas * (porcentaje / 100)
            # Eliminar cualquier registro anterior para este trabajador y rango
            historial_collection.delete_many({
                "vendedor_id": vendedor_id,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            })
            # Guardar el detalle de ventas reales en el historial
            ventas_detalle = [
                {
                    "id": v['_id'],
                    "fecha": v['fecha'],
                    "monto": v['monto']
                } for v in ventas_vendedor
            ]
            nuevo_registro = {
                "vendedor_id": vendedor_id,
                "fecha_calculo": fecha_calculo,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_ventas": total_ventas,
                "porcentaje_comision": porcentaje,
                "comision_calculada": round(comision, 2),
                "ventas_detalle": ventas_detalle
            }
            historial_collection.insert_one(nuevo_registro)
            resultados.append({
                "vendedor": object_id_to_str(vendedor),
                "ventas_en_rango": ventas_detalle,
                "total_ventas": total_ventas,
                "regla_comision": object_id_to_str(regla),
                "comision_calculada": round(comision, 2)
            })
        return jsonify({
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "resultados": resultados,
            "total_comisiones": round(sum(r['comision_calculada'] for r in resultados), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agregar-venta', methods=['POST'])
def agregar_venta():
    """Agrega una nueva venta a la colección de MongoDB."""
    try:
        data = request.get_json()
        
        # Encontrar el ID más alto y sumar 1 para simular autoincremento
        last_venta = ventas_collection.find_one(sort=[("_id", -1)])
        next_id = (last_venta['_id'] + 1) if last_venta else 1
        
        nueva_venta = {
            "_id": next_id,
            "vendedor_id": int(data['vendedor_id']),
            "fecha": data['fecha'],
            "monto": float(data['monto'])
        }
        ventas_collection.insert_one(nueva_venta)
        return jsonify({"message": "Venta agregada exitosamente", "venta": object_id_to_str(nueva_venta)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/resumen-comisiones')
def resumen_comisiones():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Fechas de inicio y fin son requeridas"}), 400
        # Buscar todos los registros del historial cuyo periodo se cruce con el rango seleccionado
        query = {
            'fecha_inicio': {'$lte': fecha_fin},
            'fecha_fin': {'$gte': fecha_inicio}
        }
        historial = list(historial_collection.find(query))
        resumen = {}
        for registro in historial:
            vid = registro['vendedor_id']
            if vid not in resumen:
                resumen[vid] = {
                    'vendedor_id': vid,
                    'comision_total': 0.0
                }
            resumen[vid]['comision_total'] += registro.get('comision_calculada', 0)
        vendedores = {v['id']: v for v in object_id_to_str(list(vendedores_collection.find()))}
        resultado = []
        for vid, data in resumen.items():
            nombre = vendedores.get(vid, {}).get('nombre', 'Desconocido')
            data['nombre'] = nombre
            resultado.append(data)
        return jsonify(sorted(resultado, key=lambda x: x['vendedor_id']))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ventas-filtradas', methods=['GET'])
def ventas_filtradas():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    if not fecha_inicio or not fecha_fin:
        return jsonify({'error': 'Debe proporcionar fecha_inicio y fecha_fin'}), 400
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except Exception:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    # Buscar ventas en el rango
    ventas = list(ventas_collection.find({
        'fecha': {'$gte': fecha_inicio, '$lte': fecha_fin}
    }))
    # Obtener vendedores y reglas
    vendedores = {v['id'] if 'id' in v else v['_id']: v for v in object_id_to_str(list(vendedores_collection.find({})))}
    reglas = {r['vendedor_id']: r for r in object_id_to_str(list(reglas_collection.find({})))}
    # Preparar respuesta
    resultado = []
    for venta in ventas:
        vendedor_id = venta['vendedor_id']
        vendedor = vendedores.get(vendedor_id)
        regla = reglas.get(vendedor_id)
        porcentaje = regla['porcentaje'] if regla else 0
        ganancia = round(venta['monto'] * porcentaje / 100, 2)
        resultado.append({
            'id': venta['_id'] if '_id' in venta else venta['id'],
            'vendedor_id': vendedor_id,
            'vendedor': vendedor['nombre'] if vendedor else 'Desconocido',
            'fecha': venta['fecha'],
            'monto': venta['monto'],
            'porcentaje': porcentaje,
            'ganancia': ganancia
        })
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 