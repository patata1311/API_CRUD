from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2023@localhost:3306/test'
db = SQLAlchemy(app)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'API de Usuarios',
    'uiversion': 3
}
swagger = Swagger(app, template_file='swagger.yaml')


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.Integer)
    estado = db.Column(db.String(20))

with app.app_context():
    db.create_all()

class UsuarioResource(Resource):
    def get(self, usuario_id):
        usuario = Usuarios.query.get(usuario_id)
        if usuario:
            return {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'telefono': usuario.telefono,
                'estado': usuario.estado
            }
        return {'message': 'Usuario no encontrado'}, 404
    
    def put(self, usuario_id):
        data = request.get_json()
        usuario = Usuarios.query.get(usuario_id)
        if usuario:
            usuario.nombre = data['nombre']
            usuario.telefono = data['telefono']
            usuario.estado = data['estado']
            db.session.commit()
            return {'message': 'Usuario actualizado'}
        api.abort(404, "Usuario no encontrado")

    def delete(self, usuario_id):
        usuario = Usuarios.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return {'message': 'Usuario eliminado'}
        api.abort(404, "Usuario no encontrado")

class CrearUsuarioResource(Resource):

    def post(self):
        data = request.get_json()
        nuevo_usuario = Usuarios(
            id=data['id'],
            nombre=data['nombre'],
            telefono=data['telefono'],
            estado=data['estado']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'message': 'Usuario creado con éxito'}

api.add_resource(UsuarioResource, '/usuarios/<int:usuario_id>')
api.add_resource(CrearUsuarioResource, '/usuarios') 

if __name__ == '__main__':
    app.run(debug=True)

