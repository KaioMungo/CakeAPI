from flask import Blueprint, request, jsonify
from errors import EmptyStringError, AuthError, IdNotExist
from models.cake_model import Cake
from config.database import db

cake_blueprint = Blueprint('cake', __name__)

@cake_blueprint.route('/cakes', methods=['POST'])
def register_cake():
    data = request.json
    try:
        required_fields = ['name', 'flavor', 'price']
        if not all(field in data for field in required_fields):
            raise KeyError("Os campos 'name', 'flavor' e 'price' são obrigatórios.")

        if not data['name'] or not data['flavor']:
            raise EmptyStringError('Nome e sabor são campos obrigatórios e não podem estar vazios.')

        if Cake.query.filter_by(name=data['name']).first():
            raise AuthError('Bolo já cadastrado com este nome.')

        new_cake = Cake(
            name=data['name'],
            flavor=data['flavor'],
            price=data['price'],
            description=data.get('description')
        )
        db.session.add(new_cake)
        db.session.commit()
        return jsonify({'Message': 'Bolo cadastrado com sucesso.'}), 201

    except (EmptyStringError, AuthError, KeyError) as e:
        return jsonify({'Error': str(e)}), 400

@cake_blueprint.route('/cakes', methods=['GET'])
def get_cakes():
    cakes = Cake.query.all()
    return jsonify([cake.to_dict() for cake in cakes])

@cake_blueprint.route('/cakes/<int:id>', methods=['GET'])
def get_cake_by_id(id):
    try:
        cake = Cake.query.get(id)
        if not cake:
            raise IdNotExist('O bolo não foi encontrado')
        return jsonify(cake.to_dict())
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@cake_blueprint.route('/cakes/<int:id>', methods=['PUT'])
def update_cake(id):
    data = request.json
    try:
        cake = Cake.query.get(id)
        if not cake:
            raise IdNotExist('O bolo não foi encontrado')

        cake.name = data.get('name', cake.name)
        cake.flavor = data.get('flavor', cake.flavor)
        cake.price = data.get('price', cake.price)
        cake.description = data.get('description', cake.description)
        cake.available = data.get('available', cake.available)

        db.session.commit()
        return jsonify({'Message': 'Bolo atualizado com sucesso.'}), 200
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404

@cake_blueprint.route('/cakes/<int:id>', methods=['DELETE'])
def delete_cake(id):
    try:
        cake = Cake.query.get(id)
        if not cake:
            raise IdNotExist('O bolo não foi encontrado')

        db.session.delete(cake)
        db.session.commit()
        return ('', 204) # Retorna 204 No Content, que é o padrão para DELETE
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404
