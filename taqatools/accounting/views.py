from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PurchaseInvoiceForm, CartItemForm, OfferForm
from products.models import Product, Price
from django.contrib.auth.models import User
from .models import CartItem
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
    price = Price.objects.filter(product=product_id).last().value
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
            discount_price = item.product.prices.last().value * (100 - item.product.prices.last().discount)/100
            no =  item.q
            item_total = discount_price * no
            total +=  item_total
        data['total'] = total
        
        json_data = json.dumps(data)
        # return render(request, 'accounting/invoices/cart.html', {'json_data': json_data})
        return HttpResponse(json_data, content_type= "application/json")

def add_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('The offer has been created Successfully!'))
            return redirect('home')
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error creating the offer' + error_message))
            return redirect('home')
    else:
        form = OfferForm()
        return render(request, 'accounting/invoices/cart.html', {'form' : form})
    
    
def search_users(request):
    request_data = json.loads(request.body)
    query = request_data['query']
    data = {}
    users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    for user in users:
        data[user.username] = f'{user.first_name} {user.last_name}'
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type= "application/json")