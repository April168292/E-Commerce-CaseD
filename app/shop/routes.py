from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.apiauthhelper import token_required

shop = Blueprint('shop',__name__, template_folder='shop_templates')

from app.models import Post, db, Product, Cart, User


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


#API STARTS HERE

@shop.route('/api/products')
def apiProducts():
    products = Product.query.all()
    return {
        'status': 'ok',
        'total_results': len(products),
        'products': [p.to_dict() for p in products]
    }

@shop.route('/api/products/<int:product_id>')
def apiSingleProduct(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return {
            'status': 'not ok',
            'total_results': 0,
        }
    return {
        'status': 'ok',
        'total_results': 1,
        'product': product.to_dict()
        }
        
@shop.route('/api/create-post', methods=["POST"])
@token_required
def apiCreatePost(user):
    data = request.json

    title = data['title']
    img_url = data['img_url']
    caption = data['caption']


    post = Post(title, img_url, caption, user.id)

    db.session.add(post)
    db.session.commit()

    return {
        'status': 'ok',
        'message': 'Successfully create a new post.',
        'post': post.to_dict()
    }



    
    

    