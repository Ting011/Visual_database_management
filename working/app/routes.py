import os
from datetime import datetime, timedelta
from . import create_app
from .models import Order, Shipment, Chip, Customer
from . import db
from flask import jsonify, redirect, request, abort, render_template, url_for, Blueprint
from flask_login import current_user, login_required, logout_user

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route("/")
@login_required
def index():
    orders = Order.query.all()
    cur_customer_id = current_user.get_id()
    cur_customer_name = Customer.query.get(cur_customer_id).customer_name
    return render_template("index.html", orders=orders, user_name = cur_customer_name)

@app.route("/ship")
@login_required
def ship():
    orders = Order.query.all()
    shipments = Shipment.query.all()
    return render_template("ship.html", orders=orders, shipments = shipments)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/order/list", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_json() for order in orders])


@app.route("/order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        abort(404)
    return render_template("order.html", order_id=order_id)


@app.route("/delete/<int:order_id>", methods=["POST"])
def delete(order_id):
    
    #delete shipment with order_id
    shipment = Shipment.query.filter(Shipment.order_id == order_id).first()
    if shipment is None:
        abort(404)
    db.session.delete(shipment)
    db.session.commit()

    #delete order with id
    order = Order.query.get(order_id)
    if order is None:
        abort(404)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for("index"))


@app.route('/add_order/', methods=['POST'])
def add_order():
    if not request.form:
        abort(400)

    # Initialize the chip
    check_chip1 = Chip.query.filter_by(chip_id = 1).first()
    if check_chip1 is None:
        chip1 = Chip(
            chip_id = 1,
            chip_type = "74HC74",
            chip_price = 30.0
        )
        db.session.add(chip1)
        db.session.commit()

    check_chip2 = Chip.query.filter_by(chip_id = 2).first()
    if check_chip2 is None:
        chip2 = Chip(
            chip_id = 2,
            chip_type = "74HC00",
            chip_price = 20.0
        )
        db.session.add(chip2)
        db.session.commit()

    check_chip3 = Chip.query.filter_by(chip_id = 3).first()
    if check_chip3 is None:
        chip3 = Chip(
            chip_id = 3,
            chip_type = "74HC04",
            chip_price = 10.0
            
        )
        db.session.add(chip3)
        db.session.commit()

     #get current customer id and address
    if current_user.is_authenticated:
        cur_customer_id = current_user.get_id()

    cur_customer_addr = Customer.query.get(cur_customer_id).customer_address

    # calculate the offset between pickup address and customer address
    if(cur_customer_addr == "Shenzhen"):
        if(request.form.get("chip_address") == "Beijing"):
            arr_date = datetime.now() + timedelta(days=1)
        elif(request.form.get("chip_address") == "Shenzhen"):
            arr_date = datetime.now() + timedelta(hours=2)
        elif(request.form.get("chip_address") == "Shanghai"):
            arr_date = datetime.now() + timedelta(hours=17)
    elif(cur_customer_addr == "Shanghai"):
        if(request.form.get("chip_address") == "Beijing"):
            arr_date = datetime.now() + timedelta(hours=14)
        elif(request.form.get("chip_address") == "Shenzhen"):
            arr_date = datetime.now() + timedelta(hours=17)
        elif(request.form.get("chip_address") == "Shanghai"):
            arr_date = datetime.now() + timedelta(hours=2)
    elif(cur_customer_addr == "Beijing"):
        if(request.form.get("chip_address") == "Beijing"):
            arr_date = datetime.now() + timedelta(hours=2)
        elif(request.form.get("chip_address") == "Shenzhen"):
            arr_date = datetime.now() + timedelta(days=1)
        elif(request.form.get("chip_address") == "Shanghai"):
            arr_date = datetime.now() + timedelta(hours=14)
    
    # add new order & shipment info into database 
    cur_chip_id = int(request.form.get('chip_id'))
    cur_order_quantity = int(request.form.get('order_quantity'))
    cp_price = Chip.query.filter_by(chip_id = cur_chip_id).first().chip_price
    total_price = float(cp_price * cur_order_quantity)

    order = Order(
        order_quantity = cur_order_quantity,
        chip_id= cur_chip_id,
        order_date = datetime.now(),
        order_price= total_price
    )

    db.session.add(order)
    db.session.commit()

    cur_order_id = Order.query.order_by(Order.order_id.desc()).first().order_id
    
    shipment = Shipment(
        shipment_date = datetime.now(),
        estimated_arrival = arr_date,
        order_id = cur_order_id
    )

    
    db.session.add(shipment)
    db.session.commit()

    return redirect(url_for("index"))


@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if not request.form:
        abort(400)
    order = Order.query.get(order_id)
    if order is None:
        abort(404)
    order.order_quantity = request.form.get('order_quantity', order.order_quantity)
    order.chip_id = request.form.get('chip_id', order.chip_id)

    update_chip_price = Chip.query.get(request.form.get('chip_id', order.chip_id)).chip_price
    update_order_price = float(update_chip_price * float(request.form.get('order_quantity', order.order_quantity)))

    order.order_price = update_order_price
    db.session.commit()
    return redirect(url_for("index"))