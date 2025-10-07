from errors import EmptyStringError, AuthError, IdNotExist
from config.database import db
from flask import Blueprint, request, jsonify
from models.order_model import Order
from models.order_item_model import OrderItem
from models.cake_model import Cake

order_item_blueprint = Blueprint('order_item', __name__)

def _update_order_total_price(order_id):
    order = Order.query.get(order_id)
    if not order:
        return 

    total_price = sum(item.quantity * item.unit_price for item in order.items)
    order.total_price = total_price
    db.session.commit()

@order_item_blueprint.route('/order-items', methods=['POST'])
def add_order_item():
    data = request.json
    try:
        if 'order_id' not in data or 'cake_id' not in data or 'quantity' not in data:
            raise KeyError("Campos 'order_id', 'cake_id' e 'quantity' são obrigatórios.")
        
        order = Order.query.get(data['order_id'])
        if not order:
            raise IdNotExist(f"Pedido com ID {data['order_id']} não encontrado.")
        
        cake = Cake.query.get(data['cake_id'])
        if not cake:
            raise IdNotExist(f"Bolo com ID {data['cake_id']} não encontrado.")

        unit_price = cake.price 
        
        new_item = OrderItem(
            order_id=data['order_id'],
            cake_id=data['cake_id'],
            quantity=data['quantity'],
            unit_price=unit_price
        )

        db.session.add(new_item)
        db.session.commit()
        
        _update_order_total_price(data['order_id'])
        
        return jsonify(new_item.to_dict()), 201

    except (KeyError, IdNotExist) as e:
        return jsonify({'Error': str(e)}), 400
    

@order_item_blueprint.route('/orders/<int:order_id>/items', methods=['GET'])
def get_order_items_by_order_id(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify([item.to_dict() for item in items])

@order_item_blueprint.route('/order-items/<int:order_item_id>', methods=['PUT'])
def update_order_item_quantity(order_item_id):
    data = request.json
    try:
        if 'quantity' not in data:
            raise KeyError("O campo 'quantity' é obrigatório.")

        new_quantity = data['quantity']
        if not isinstance(new_quantity, int) or new_quantity <= 0:
            raise ValueError("A quantidade deve ser um número inteiro positivo.")

        item = OrderItem.query.get(order_item_id)
        if not item:
            raise IdNotExist('Item do pedido não encontrado.')

        item.quantity = new_quantity
        db.session.commit()
        _update_order_total_price(item.order_id) 
        
        return jsonify({'Message': 'Item do pedido atualizado com sucesso.'}), 200

    except (KeyError, ValueError, IdNotExist) as e:
        return jsonify({'Error': str(e)}), 400
    except Exception as e:
        return jsonify({'Error': 'Ocorreu um erro inesperado.'}), 500

@order_item_blueprint.route('/order-items/<int:order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    try:
        item = OrderItem.query.get(order_item_id)

        if not item:
            raise IdNotExist('Item do pedido não encontrado.')
        
        order_id_to_update = item.order_id
        
        db.session.delete(item)
        db.session.commit()
        
        _update_order_total_price(order_id_to_update)

        return jsonify({'Message': 'Item do pedido deletado com sucesso.'}), 200

    except IdNotExist as e:
        return jsonify({'Error': str(e)}), 404