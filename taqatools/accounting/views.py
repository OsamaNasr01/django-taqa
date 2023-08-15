from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PurchaseInvoiceForm, CartItemForm, OfferForm, OfferItemForm, SaleItemForm, SaleForm
from .forms import PurchaseItemForm, PurchaseForm
from products.models import Product, Price
from django.contrib.auth.models import User
from .models import CartItem, Offer, SaleInvoice,PurchaseInvoice
import json
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def accounting(request):
    return render(request, 'accounting/invoices/accounting_panel.html', {})


def add_s_invoice(request):
    if request.method == 'POST':
        invoice_form = PurchaseInvoiceForm(request.POST)
        return render(request, 'accounting/invoices/add_s_invoice.html', {
        'invoice_form': invoice_form,
    })
    else:
        invoice_form = PurchaseInvoiceForm()
        return render(request, 'accounting/invoices/add_s_invoice.html', {
        'invoice_form': invoice_form,
    })
        
def add_product_cart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    price = Price.objects.filter(product=product_id).last().value *(100 - Price.objects.filter(product=product_id).last().discount)/100
    user = request.user
    no = int(data['no'])    
    in_cart = product.cart.filter(user=request.user)
    if not in_cart:
        form = CartItemForm()
        item= form.save(commit=False)
        item.product = product
        item.user = user
        item.q = int(no)
        item.price = price
        item.save()
        print(user)
        return_data = {
            'cart_items': CartItem.objects.filter(user=user).count(),
            'message' : f'{product.name} is added successfuly to the Cart',
        }
        json_data= json.dumps(return_data)
        print(json_data)
        return HttpResponse(json_data, content_type= "application/json")
    else:
        item = CartItem.objects.filter(user=request.user).filter(product=product)
        if request.method == 'POST':
            item.delete()
            return_data = {
                'cart_items': CartItem.objects.filter(user=user).count(),
                'message' : f'{product.name} is removed from Cart successfuly',
            }
            json_data= json.dumps(return_data)
            return HttpResponse(json_data, content_type= "application/json")
            

def cart(request):
    items = CartItem.objects.filter(user=request.user)
    offer_form = OfferForm()
    i=0
    data={}
    total = 0
    data_items = {}
    for item in items:
        price = item.price
        no =  item.q
        item_total = price * no
        total +=  item_total
        i+=1
        x= {
            'name': item.product.name,
            'price': price,
            'no': no,
            'total':  item_total,
            'id': item.id,
            'slug': item.product.slug,
            
        }
        data_items[i] = x
    data['total'] = total
    data['items'] = data_items
        
    json_data = json.dumps(data)
    print(json_data)
    return render(request, 'accounting/invoices/cart.html', {
        'json_data': json_data,
        'form' :offer_form,
        })


def delete_cart_item(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        items = CartItem.objects.filter(user=request.user)
        i=0
        total = 0
        data={}
        data_items = {}
        for item in items:
            discount_price = item.product.prices.last().value * (100 - item.product.prices.last().discount)/100
            no =  item.q
            item_total = discount_price * no
            total +=  item_total
            i+=1
            x= {
                'name': item.product.name,
                'price': discount_price,
                'no': no,
                'total':  item_total,
                'id': item.id,
                'slug': item.product.slug,
                
            }
            data_items[i] = x
        data['total'] = total
        data['items'] = data_items
            
        json_data = json.dumps(data)
        # return render(request, 'accounting/invoices/cart.html', {'json_data': json_data})
        return HttpResponse(json_data, content_type= "application/json")

def update_cart_item(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    new_q = data['new_q']
    item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        item.q = new_q
        item.save()
        items = CartItem.objects.filter(user=request.user)
        total = 0
        for item in items:
            price = item.price
            no =  item.q
            item_total = price * no
            total +=  item_total
        data['total'] = total
        
        json_data = json.dumps(data)
        # return render(request, 'accounting/invoices/cart.html', {'json_data': json_data})
        return HttpResponse(json_data, content_type= "application/json")

def add_offer(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = OfferForm()
        offer  = form.save(commit=False)
        print(data)
        username = data['user_name']
        user = User.objects.get(username = username)
        offer.user = user
        offer.description = data['description']
        offer.value = data['cart_total_value']
        cart_items = CartItem.objects.filter(user = request.user)
        offer.save()
        for item in cart_items:
            item_form = OfferItemForm()
            offer_item= item_form.save(commit=False)
            offer_item.product = item.product
            offer_item.offer = Offer.objects.last()
            offer_item.q = item.q
            offer_item.price = item.price
            offer_item.save()
            cart_item = CartItem.objects.get(id = item.id)
            cart_item.delete()
        messages.success(request, ('The offer has been created Successfully!'))
        return HttpResponse({'ok':"ok"})
    
    
def search_users(request):
    request_data = json.loads(request.body)
    query = request_data['query']
    data = {}
    users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    for user in users:
        data[user.username] = f'{user.first_name} {user.last_name} {user.username}'
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type= "application/json")

def offers(request):
    offers = Offer.objects.all()
    return render(request, 'accounting/offers/offers.html', {'offers':offers})


def offer_profile(request, id):
    offer = Offer.objects.get(id=id)
    total = {}
    for item in offer.items.all():
        total[f'total_{item.id}'] = item.price*item.q
        
    return render(request, 'accounting/offers/offer_profile.html', {
        'offer':offer,
        'total':json.dumps(total)
        })
    
def user_offers(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user':user}
    return render(request, 'accounting/offers/user_offers.html', context)

def add_sale(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = SaleForm()
        invoice  = form.save(commit=False)
        username = data['user_name']
        user = User.objects.get(username = username)
        invoice.user = user
        invoice.description = data['description']
        invoice.value = data['cart_total_value']
        print(invoice.value)
        cart_items = CartItem.objects.filter(user = request.user)
        invoice.save()
        for item in cart_items:
            item_form = SaleItemForm()
            sale_item= item_form.save(commit=False)
            sale_item.product = item.product
            sale_item.invoice = SaleInvoice.objects.last()
            sale_item.q = item.q
            sale_item.price = item.price
            sale_item.save()
            cart_item = CartItem.objects.get(id = item.id)
            cart_item.delete()
        messages.success(request, ('The invoice has been created Successfully!'))
        return HttpResponse({'ok':"ok"})
    
    
def add_purchase(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = PurchaseForm()
        invoice  = form.save(commit=False)
        username = data['user_name']
        print(username)
        user = User.objects.get(username = username)
        invoice.user = user
        invoice.description = data['description']
        print(data['cart_total_value'])
        invoice.value = data['cart_total_value']
        cart_items = CartItem.objects.filter(user = request.user)
        invoice.save()
        for item in cart_items:
            item_form = PurchaseItemForm()
            purchase_item= item_form.save(commit=False)
            purchase_item.product = item.product
            purchase_item.invoice = PurchaseInvoice.objects.last()
            purchase_item.q = item.q
            purchase_item.price = item.price
            purchase_item.save()
            cart_item = CartItem.objects.get(id = item.id)
            cart_item.delete()
        messages.success(request, ('The invoice has been created Successfully!'))
        return HttpResponse({'ok':"ok"})
    
    
def sale_profile(request, id):
    invoice = SaleInvoice.objects.get(id=id)
    total = {}
    for item in invoice.items.all():
        total[f'total_{item.id}'] = item.price*item.q
        
    return render(request, 'accounting/sales/sale_profile.html', {
        'invoice':invoice,
        'total':json.dumps(total)
        })
    

def sales(request):
    invoices = SaleInvoice.objects.all()
    return render(request, 'accounting/sales/sales.html', {'invoices':invoices})


    
def user_sales(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user':user}
    return render(request, 'accounting/sales/user_sales.html', context)

    
def purchase_profile(request, id):
    invoice = PurchaseInvoice.objects.get(id=id)
    total = {}
    for item in invoice.items.all():
        total[f'total_{item.id}'] = item.price*item.q
        
    return render(request, 'accounting/purchases/purchase_profile.html', {
        'invoice':invoice,
        'total':json.dumps(total)
        })
    

def purchases(request):
    invoices = PurchaseInvoice.objects.all()
    return render(request, 'accounting/purchases/purchases.html', {'invoices':invoices})


    
def user_purchases(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user':user}
    return render(request, 'accounting/purchases/user_purchases.html', context)
