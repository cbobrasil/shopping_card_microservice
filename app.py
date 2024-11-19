from flask import Flask
from cart.routes import cart_blueprint
from aws_lambda_wsgi import LambdaMiddleware

app = Flask(__name__)
app.register_blueprint(cart_blueprint, url_prefix="/cart")
app.wsgi_app = LambdaMiddleware(app.wsgi_app)  # Make Flask compatible with Lambda

def lambda_handler(event, context):
    from aws_lambda_wsgi import response
    return response(app, event, context)
