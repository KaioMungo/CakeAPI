from config.database import app, db
from flask import jsonify
from controllers.cake_controller import cake_blueprint
from controllers.custumer_controller import custumer_blueprint
from controllers.order_controller import order_blueprint
from controllers.order_item_controller import order_item_blueprint
from errors import IdNotExist

app.register_blueprint(cake_blueprint)
app.register_blueprint(custumer_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(order_item_blueprint)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
