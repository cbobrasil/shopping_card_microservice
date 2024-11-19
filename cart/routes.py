from flask import Blueprint, request, jsonify
from cart.models import ShoppingCart

cart_blueprint = Blueprint("cart", __name__)
shopping_cart = ShoppingCart()

@cart_blueprint.route("/add", methods=["POST"])
def add_item():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    quantity = data.get("quantity", 1)
    if not user_id or not item_id:
        return jsonify({"error": "User ID and Item ID are required"}), 400
    try:
        shopping_cart.add_item(user_id, item_id, quantity)
        return jsonify({"message": "Item added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cart_blueprint.route("/remove", methods=["POST"])
def remove_item():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    if not user_id or not item_id:
        return jsonify({"error": "User ID and Item ID are required"}), 400
    try:
        shopping_cart.remove_item(user_id, item_id)
        return jsonify({"message": "Item removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cart_blueprint.route("/", methods=["GET"])
def get_cart():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    try:
        cart = shopping_cart.get_cart(user_id)
        return jsonify({"cart": cart}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
