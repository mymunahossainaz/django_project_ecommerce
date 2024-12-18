from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home page view
def home(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'home.html', {'products': products})

# Carousel view for images
def carousel_view(request):
    images = [
        {'src': '/static/images/g1.jpg', 'alt': 'Banner 1'},
        {'src': '/static/images/g2.jpg', 'alt': 'Banner 2'},
        {'src': '/static/images/g3.jpg', 'alt': 'Banner 3'},
    ]
    return render(request, 'home.html', {'images': images})

# Shop view with pagination
def shop(request):
    products_list = [
        {"id": 1, "name": "Honey", "price": 700, "image": "images/honey.jpg"},
        {"id": 2, "name": "Vegetable", "price": 100, "image": "images/vegetable.jpg"},
        {"id": 3, "name": "Shampoo", "price": 250, "image": "images/sampoo.png"},
        {"id": 4, "name": "Meat", "price": 1200, "image": "images/meat.jpg"},
        {"id": 5, "name": "Egg", "price": 10, "image": "images/egg.png"},
        {"id": 6, "name": "Milk", "price": 50, "image": "images/milk.jpg"},
    ]
    paginator = Paginator(products_list, 3)  # Show 3 products per page
    page_number = request.GET.get('page')

    try:
        products = paginator.get_page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop.html', {'products': products})

# Product detail page view
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)  # Fetch the product based on the ID
    related_products = Product.objects.exclude(id=id)[:4]  # Get 4 related products
    return render(request, 'product_detail.html', {'product': product, 'products': related_products})

# Cart view to show user's cart items
# Make sure you have a view function named `cart_view`
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Adjust as per your cart model
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 5.00 if cart_items else 0.00  # Example fixed shipping fee
    total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    }
    return render(request, "cart.html", context)


# Update the quantity of an item in the cart
def update_cart(request, product_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if quantity:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
    return redirect("cart")

# Remove an item from the cart
def remove_cart(request, product_id):
    if request.method == "POST":
        cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect("cart")

# Get or create a cart for the user (whether authenticated or anonymous)
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id  # Save cart ID to the session
    return cart

# Add honey to the cart (example product)
def add_honey_to_cart(request):
    honey = Product.objects.get(name="Honey")  # Get the Honey product
    cart = get_or_create_cart(request)  # Get or create the user's cart
    cart.add(honey)  # Add honey to the cart
    return redirect('cart')

# Add milk to the cart
def add_milk_to_cart(request):
    milk = Product.objects.get(name="Milk")  # Get the Milk product
    cart = get_or_create_cart(request)  # Get or create the user's cart
    cart.add(milk)  # Add milk to the cart
    return redirect('cart')

# Add shampoo to the cart
def add_shampoo_to_cart(request):
    shampoo = Product.objects.get(name="Shampoo")  # Get the Shampoo product
    cart = get_or_create_cart(request)  # Get or create the user's cart
    cart.add(shampoo)  # Add shampoo to the cart
    return redirect('cart')

# View to add a product to the cart by product ID
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get product by ID
    cart = get_or_create_cart(request)  # Get or create the user's cart
    cart.add(product)  # Add the product to the cart
    return redirect('cart')

# Cart page view to show the cart content
def cart_page(request):
    cart = get_or_create_cart(request)  # Get the user's cart
    return render(request, 'shop/cart.html', {'cart': cart})
