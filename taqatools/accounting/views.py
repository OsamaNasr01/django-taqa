from django.shortcuts import render, HttpResponse
from .forms import PurchaseInvoiceForm, CartItemForm
from products.models import Product, Price
from django.contrib.auth.models import User
import json

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
    form = CartItemForm()
    x= form.save(commit=False)
    x.product = product
    x.user = user
    x.q = 1
    x.price = price
    x.save()
    print(user)
    return HttpResponse('ok')
    