from flask import Flask, request, jsonify
from models import db, Usuario, Producto, Orden
from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ordenes.db'
db.init_app(app)

q = Queue(connection=Redis(host='redis', port=6379, db=0))

@app.route('/ordenes', methods=['POST'])
def crear_orden():
    data = request.get_json()
    if not data or 'usuario' not in data or 'producto' not in data or 'cantidad' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    usuario = Usuario.query.get(data['usuario'])
    print("USUARIO:", data['usuario'])
    producto = Producto.query.get(data['producto'])

    if usuario is None:
        return jsonify({'error': 'El usuario no existe'}), 400
    
    if producto is None:
        return jsonify({'error': 'El producto no existe'}), 400

    nueva = Orden(usuario=data['usuario'], producto=data['producto'], cantidad=data['cantidad'], estado="procesando")
    db.session.add(nueva)
    db.session.commit()
    return jsonify({
        'id': nueva.id,
        'usuario': nueva.usuario,
        'producto': nueva.producto,
        'cantidad': nueva.cantidad,
        'estado': nueva.estado
    }), 201

@app.route('/ordenes', methods=['GET'])
def listar_ordenes():
    ordenes = Orden.query.all()
    return jsonify([
        {
            'id': o.id,
            'usuario': o.usuario,
            'producto': o.producto,
            'cantidad': o.cantidad,
            'estado': o.estado
        }
        for o in ordenes
    ])

@app.route('/ordenes/<int:orden_id>', methods=['GET'])
def obtener_orden(orden_id):
    orden = Orden.query.get_or_404(orden_id)
    return jsonify({
        'id': orden.id,
        'usuario': orden.usuario,
        'producto': orden.producto,
        'cantidad': orden.cantidad,
        'estado': orden.estado
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
