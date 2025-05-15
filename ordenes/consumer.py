from models import Producto, Usuario, db
from app import app 

def consumer_product(product_data):
    with app.app_context():
        product = Producto(
            id=product_data['id'],
            nombre=product_data['nombre'],
            precio=product_data['precio'],
            stock=product_data['stock']
        )
        db.session.add(product)
        db.session.commit()

def consumer_user(user_data):
    with app.app_context():
        user = Usuario(
            id=user_data['id'],
            nombre=user_data['nombre'],
            correo=user_data['correo']
        )
        db.session.add(user)
        db.session.commit()