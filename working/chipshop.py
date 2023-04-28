from app import db
from app.routes import app
from app.models import Order
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Order=Order)