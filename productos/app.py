from flask import Flask, request, jsonify
from models import db, Producto
from redis import Redis
from rq import Queue
from consumer import consumer_product



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
db.init_app(app)

q = Queue(connection=Redis(host='redis', port=6379, db=0))

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nuevo = Producto(nombre=data['nombre'], precio=data['precio'], stock=data['stock'])
    db.session.add(nuevo)
    db.session.commit()
    q.enqueue(consumer_product, {
        'id': nuevo.id,
        'nombre': nuevo.nombre,
        'precio': nuevo.precio,
        'stock': nuevo.stock
    })
    return jsonify({
        'id': nuevo.id,
        'nombre': nuevo.nombre,
        'precio': nuevo.precio,
        'stock': nuevo.stock
    }), 201

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return jsonify([
        {'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'stock': p.stock}
        for p in productos
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
