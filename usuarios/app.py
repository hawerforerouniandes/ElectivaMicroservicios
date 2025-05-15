from flask import Flask, request, jsonify
from models import db, Usuario
from redis import Redis
from rq import Queue
from consumer import consumer_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

q = Queue(connection=Redis(host='redis', port=6379, db=0))

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if not data or 'nombre' not in data or 'correo' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nuevo = Usuario(nombre=data['nombre'], correo=data['correo'])
    db.session.add(nuevo)
    db.session.commit()
    q.enqueue(consumer_user, {
        'id': nuevo.id,
        'nombre': nuevo.nombre,
        'correo': nuevo.correo
    })

    return jsonify({'id': nuevo.id, 'nombre': nuevo.nombre, 'correo': nuevo.correo}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {'id': u.id, 'nombre': u.nombre, 'correo': u.correo}
        for u in usuarios
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
