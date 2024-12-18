class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        if product.id not in self.cart:
            self.cart[product.id] = {
                'name': product.name,
                'price': product.price,
                'quantity': 1,
            }
        else:
            self.cart[product.id]['quantity'] += 1

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['quantity'] * item['price'] for item in self.cart.values())
