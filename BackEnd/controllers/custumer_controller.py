from errors import EmptyStringError, AuthError, IdNotExist
from config.database import db
from models.custumer_model import Customer
from flask import Blueprint, request, jsonify

custumer_blueprint = Blueprint('custumer', __name__)

@custumer_blueprint.route('/register-customer', methods=['POST'])
def register_customer():
    data = request.json
    try:
        if 'name' not in data:
            raise KeyError("O campo 'name' é obrigatório.")
        
        if not data['name'] or data['name'].strip() == '':
            raise EmptyStringError('O nome do cliente precisa ser preenchido.')
        
        customer = Customer.query.filter_by(name=data['name']).first()
        if customer:
            raise AuthError('Cliente já cadastrado com este nome.')
        
        new_customer = Customer(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )

        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_dict()), 201

    except (KeyError, EmptyStringError, AuthError) as e:
        return jsonify({'Error': str(e)}), 400

@custumer_blueprint.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])


@custumer_blueprint.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    try:
        customer = Customer.query.get(id)
        if not customer:
            raise IdNotExist('O cliente não foi encontrado.')
        return jsonify(customer.to_dict())
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404
    

@custumer_blueprint.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    try:
        customer = Customer.query.get(id)
        if not customer:
            raise IdNotExist('O cliente não foi encontrado.')
        
        customer.name = data.get('name', customer.name) 
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)
        db.session.commit()
        return jsonify({'Message': 'Cliente atualizado com sucesso.'}), 200
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404
    

@custumer_blueprint.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get(id)
        if not customer:
            raise IdNotExist('O cliente não foi encontrado.')
        
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'Message': 'Cliente deletado com sucesso.'}), 200
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404