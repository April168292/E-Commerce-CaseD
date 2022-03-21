from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

shop = Blueprint('shop',__name__, template_folder='shop_templates')

from app.models import db, Product, Cart


@shop.route('/products')
def allProducts():
    products = Product.query.all()
    return render_template('shop.html', products= products)

@shop.route('/products/<int:product_id>')
def individualProduct(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return redirect(url_for('shop.allProducts'))
    return render_template('individual_product.html', product = product)

# CART FUNCTIONALITY
@shop.route('/cart')
def showcart():
    cart = Cart.query.filter_by(user_id=current_user.id)
    count = {}
    for item in cart:
        count[item.product_id] = count.get(item.product_id, 0) + 1
    
    cart_products = []
    for product_id in count:
        product_info = Product.query.filter_by(id=product_id).first().to_dict()
        product_info["quantity"] = count[product_id]
        product_info['subtotal'] = product_info['quantity'] * product_info['price']
        cart_products.append(product_info)

    return render_template('show_cart.html', cart = cart_products)

@shop.route('/cart/add<int:product_id>')
def addtocart(product_id):
    cart_item = Cart(current_user.id, product_id)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('shop.allProducts'))

@shop.route('/cart/add', methods=["POST"])
def addtocart2():
    print(request.data)
    # cart_item = Cart(current_user.id, product_id)
    # db.session.add(cart_item)
    # db.session.commit()
    return redirect(url_for('shop.allProducts'))



