from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Item
from .models import Cart, CartItem

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'cart/view_cart.html', context)

@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1  
    cart_item.save()

    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, item__id=item_id)
    cart_item.delete()

    return redirect('cart:view_cart')

@login_required
def update_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, item__id=item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is invalid or zero

    return redirect('cart:view_cart')  

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/checkout.html', {'cart': cart})
