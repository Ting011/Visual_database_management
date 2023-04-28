from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id')) # Set this as the login customer_id
    order_date = db.Column(db.DateTime, nullable=True)
    chip_id = db.Column(db.Integer, db.ForeignKey('chips.chip_id'))
    order_quantity = db.Column(db.Integer, nullable=False) # Chip Wafers ordered
    order_price = db.Column(db.Float, nullable=True) # Look up price of chip type based on chip id
    #address = relationship("Address", cascade="all, delete")


    def to_json(self):
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'order_date': self.order_date,
            'chip_id': self.chip_id,
            'order_quantity': self.order_quantity,
            'order_price': self.order_price
        }

class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_password = db.Column(db.String(200), nullable=False)
    customer_address = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='customer')

    def to_json(self):
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_password': self.customer_password,
            'customer_address': self.address
        }

    def get_id(self):
        return (self.customer_id)

    def set_password(self, password):
        # Create hashed password
        self.customer_password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.customer_password, password)

    def __repr__(self):
        return '<Customer {}>'.format(self.username)

class Chip(db.Model):
    __tablename__ = 'chips'
    chip_id = db.Column(db.Integer, primary_key=True)
    chip_type = db.Column(db.String(100), nullable=False)
    chip_price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='chip') # One chip can be used in many orders

    def to_json(self):
        return {
            'chip_id': self.chip_id,
            'chip_type': self.chip_type,
            'chip_price': self.chip_price
        }

class Plant(db.Model):
    _tablename__ = 'plants'
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_location = db.Column(db.String(100), nullable=False)
    plant_type = db.Column(db.String(100), nullable=False)
    plant_capacity = db.Column(db.Integer, nullable=False)
    plant_order = db.Column(db.Integer, nullable=True) # Currently processing order, can't be foreign key because deleting order will delete plant

    def to_json(self):
        return {
            'plant_id': self.plant_id,
            'plant_location': self.plant_location,
            'plant_type': self.plant_type,
            'plant_capacity': self.plant_capacity,
            'plant_order': self.plant_order
        }

class Shipment(db.Model):
    __tablename__ = 'shipments'
    shipment_id = db.Column(db.Integer, primary_key=True)
    shipment_date = db.Column(db.DateTime, nullable=False) # Calculate from order_date + (order_quantity / plant_capacity) * 24 hours
    estimated_arrival = db.Column(db.DateTime, nullable=False) # Calculated from shipment_date + (plant_location - customer_address) * speed coefficient
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    # plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    # # I dont know if these are needed, but Copilot recommended them
    # order = db.relationship('Order', backref='shipment') # One order can be shipped from many plants
    # plant = db.relationship('Plant', backref='shipment') # One plant can ship many orders

    def to_json(self):
        return {
            'shipment_id': self.shipment_id,
            'shipment_date': self.shipment_date,
            'estimated_arrival': self.estimated_arrival,
            # 'order_id': self.order_id,
            # 'plant_id': self.plant_id
        }