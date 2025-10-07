from errors import EmptyStringError, AuthError, IdNotExist
from config.database import db
from models.custumer_model import Customer
from models.order_model import Order
from flask import Blueprint, request, jsonify

order_blueprint = Blueprint('order',__name__)

@order_blueprint.route('/register-order', methods=['POST'])
def register_order():
    data = request.json
    try:
        if 'customer_id' not in data:
            raise KeyError("O campo 'customer_id' é obrigatório.")
        
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            raise IdNotExist(f"Cliente com ID {data['customer_id']} não encontrado. O pedido não pode ser criado.")

        
        new_order = Order(
            customer_id=data['customer_id'],
            total_price=0, 
            delivery_date=data.get('delivery_date'), 
            status=data.get('status', 'Pendente') 
        )

        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), 201
    except (KeyError, IdNotExist) as e:
        return jsonify({'Error': str(e)}), 400

@order_blueprint.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])


@order_blueprint.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    try:
        order = Order.query.get(id)
        if not order:
            raise IdNotExist('O pedido não foi encontrado.')
        return jsonify(order.to_dict())
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404
    

@order_blueprint.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.json
    try:
        order = Order.query.get(id)
        if not order:
            raise IdNotExist('O pedido não foi encontrado.')
        order.status = data.get('status', order.status) 
        order.delivery_date = data.get('delivery_date', order.delivery_date)
        db.session.commit()
        return jsonify({'Message': 'Pedido atualizado com sucesso.'}), 200
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404


@order_blueprint.route('/orders/<int:id>', methods=['DELETE'])   
def delete_order(id):
    try:
        order = Order.query.get(id)
        if not order:
            raise IdNotExist('O pedido não foi encontrado.')
        
        db.session.delete(order)
        db.session.commit()
        return jsonify({'Message': 'Pedido deletado com sucesso.'}), 200
    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404