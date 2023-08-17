from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PurchaseInvoiceForm, CartItemForm, OfferForm, OfferItemForm, SaleItemForm, SaleForm
from .forms import PurchaseItemForm, PurchaseForm, CreditForm, DepitForm
from products.models import Product, Price
from django.contrib.auth.models import User
from .models import CartItem, Offer, SaleInvoice, PurchaseInvoice, Credit, Depit
import json
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from members.views import user_profile

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
    price = Price.objects.filter(product=product_id).last(
    ).value * (100 - Price.objects.filter(product=product_id).last().discount)/100
    user = request.user
    no = int(data['no'])
    in_cart = product.cart.filter(user=request.user)
    if not in_cart:
        form = CartItemForm()
        item = form.save(commit=False)
        item.product = product
        item.user = user
        item.q = int(no)
        item.price = price
        item.save()
        print(user)
        return_data = {
            'cart_items': CartItem.objects.filter(user=user).count(),
            'message': f'{product.name} is added successfuly to the Cart',
        }
        json_data = json.dumps(return_data)
        print(json_data)
        return HttpResponse(json_data, content_type="application/json")
    else:
        item = CartItem.objects.filter(
            user=request.user).filter(product=product)
        if request.method == 'POST':
            item.delete()
            return_data = {
                'cart_items': CartItem.objects.filter(user=user).count(),
                'message': f'{product.name} is removed from Cart successfuly',
            }
            json_data = json.dumps(return_data)
            return HttpResponse(json_data, content_type="application/json")


def cart(request):
    items = CartItem.objects.filter(user=request.user)
    offer_form = OfferForm()
    i = 0
    data = {}
    total = 0
    data_items = {}
    for item in items:
        price = item.price
        no = item.q
        item_total = price * no
        total += item_total
        i += 1
        x = {
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
        'form': offer_form,
    })


def delete_cart_item(request):
    data = json.loads(request.body)
    item_id = data['item_id']
    item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        items = CartItem.objects.filter(user=request.user)
        i = 0
        total = 0
        data = {}
        data_items = {}
        for item in items:
            discount_price = item.product.prices.last(
            ).value * (100 - item.product.prices.last().discount)/100
            no = item.q
            item_total = discount_price * no
            total += item_total
            i += 1
            x = {
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
        return HttpResponse(json_data, content_type="application/json")


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
            no = item.q
            item_total = price * no
            total += item_total
        data['total'] = total

        json_data = json.dumps(data)
        # return render(request, 'accounting/invoices/cart.html', {'json_data': json_data})
        return HttpResponse(json_data, content_type="application/json")


def add_offer(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = OfferForm()
        offer = form.save(commit=False)
        print(data)
        username = data['user_name']
        user = User.objects.get(username=username)
        offer.user = user
        offer.description = data['description']
        cart_items = CartItem.objects.filter(user=request.user)
        offer.save()
        for item in cart_items:
            item_form = OfferItemForm()
            offer_item = item_form.save(commit=False)
            offer_item.product = item.product
            offer_item.offer = Offer.objects.last()
            offer_item.q = item.q
            offer_item.price = item.price
            offer_item.save()
            cart_item = CartItem.objects.get(id=item.id)
            cart_item.delete()
        messages.success(request, ('The offer has been created Successfully!'))
        return HttpResponse({'ok': "ok"})



def offer_update(request, id):
    offer = get_object_or_404(SaleInvoice, id=id)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(
                request, ('The offer has been Updated Successfully!'))
            return offer_profile(request, id)


def offer_delete(request, id):
    offer = get_object_or_404(Offer, id=id)
    if request.method == 'POST':
        offer.delete()
        messages.success(
            request, ('The offer has been Deleted Successfully!'))
        return redirect('offers')



def search_users(request):
    request_data = json.loads(request.body)
    query = request_data['query']
    data = {}
    users = User.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query))
    for user in users:
        data[user.username] = f'{user.first_name} {user.last_name} {user.username}'
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")


def offers(request):
    offers = Offer.objects.all()
    return render(request, 'accounting/offers/offers.html', {'offers': offers})


def offer_profile(request, id):
    offer = Offer.objects.get(id=id)
    total = {}
    for item in offer.items.all():
        total[f'total_{item.id}'] = item.price*item.q

    return render(request, 'accounting/offers/offer_profile.html', {
        'offer': offer,
        'total': json.dumps(total)
    })


def user_offers(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'accounting/offers/user_offers.html', context)


def sale_profile(request, id):
    invoice = SaleInvoice.objects.get(id=id)
    form = SaleForm(instance=invoice)

    return render(request, 'accounting/sales/sale_profile.html', {
        'invoice': invoice,
        'form': form
    })


def sales(request):
    invoices = SaleInvoice.objects.all()
    return render(request, 'accounting/sales/sales.html', {'invoices': invoices})


def user_sales(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'accounting/sales/user_sales.html', context)


def add_sale(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = SaleForm()
        invoice = form.save(commit=False)
        username = data['user_name']
        user = User.objects.get(username=username)
        invoice.user = user
        invoice.description = data['description']
        cart_items = CartItem.objects.filter(user=request.user)
        invoice.save()
        for item in cart_items:
            item_form = SaleItemForm()
            sale_item = item_form.save(commit=False)
            sale_item.product = item.product
            sale_item.invoice = SaleInvoice.objects.last()
            sale_item.q = item.q
            sale_item.price = item.price
            sale_item.save()
            cart_item = CartItem.objects.get(id=item.id)
            cart_item.delete()
        messages.success(
            request, ('The invoice has been created Successfully!'))
        return HttpResponse({'ok': "ok"})


def sale_update(request, id):
    invoice = get_object_or_404(SaleInvoice, id=id)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(
                request, ('The Invoice has been Updated Successfully!'))
            return sale_profile(request, id)


def sale_delete(request, id):
    invoice = get_object_or_404(SaleInvoice, id=id)
    if request.method == 'POST':
        invoice.delete()
        messages.success(
            request, ('The Invoice has been Deleted Successfully!'))
        return redirect('sales')


def add_purchase(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        form = PurchaseForm()
        invoice = form.save(commit=False)
        username = data['user_name']
        print(username)
        user = User.objects.get(username=username)
        invoice.user = user
        invoice.description = data['description']
        cart_items = CartItem.objects.filter(user=request.user)
        invoice.save()
        for item in cart_items:
            item_form = PurchaseItemForm()
            purchase_item = item_form.save(commit=False)
            purchase_item.product = item.product
            purchase_item.invoice = PurchaseInvoice.objects.last()
            purchase_item.q = item.q
            purchase_item.price = item.price
            purchase_item.save()
            cart_item = CartItem.objects.get(id=item.id)
            cart_item.delete()
        messages.success(
            request, ('The invoice has been created Successfully!'))
        return HttpResponse({'ok': "ok"})


def purchase_update(request, id):
    invoice = get_object_or_404(PurchaseInvoice, id=id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(
                request, ('The Invoice has been Updated Successfully!'))
            return purchase_profile(request, id)


def purchase_delete(request, id):
    invoice = get_object_or_404(PurchaseInvoice, id=id)
    if request.method == 'POST':
        invoice.delete()
        messages.success(
            request, ('The Invoice has been Deleted Successfully!'))
        return redirect('purchases')


def purchase_profile(request, id):
    invoice = PurchaseInvoice.objects.get(id=id)
    total = {}
    for item in invoice.items.all():
        total[f'total_{item.id}'] = item.price*item.q

    return render(request, 'accounting/purchases/purchase_profile.html', {
        'invoice': invoice,
        'total': json.dumps(total)
    })


def purchases(request):
    invoices = PurchaseInvoice.objects.all()
    return render(request, 'accounting/purchases/purchases.html', {'invoices': invoices})


def user_purchases(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'accounting/purchases/user_purchases.html', context)


def payment_profile(request, id):
    payment = Credit.objects.get(id=id)
    form = CreditForm(instance=payment)

    return render(request, 'accounting/payments/payment_profile.html', {
        'payment': payment,
        'form': form,
    })


def payments(request):
    payments = Credit.objects.all()
    return render(request, 'accounting/payments/payments.html', {'payments': payments})


def user_payments(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'accounting/payments/user_payments.html', context)


def add_payment(request, username):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        user = User.objects.get(username=username)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.description = request.POST['description']
            payment.value = request.POST['value']
            payment.user = user
            payment.save()
            messages.success(
                request, ('The Payment has been Added Successfully!'))
            return user_profile(request, username)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error ' + error_message))
            return user_profile(request, username)


def payment_update(request, id):
    payment = get_object_or_404(Credit, id=id)
    if request.method == 'POST':
        form = CreditForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(
                request, ('The Payment has been Updated Successfully!'))
            return payment_profile(request, id)


def payment_delete(request, id):
    payment = get_object_or_404(Credit, id=id)
    if request.method == 'POST':
        payment.delete()
        messages.success(
            request, ('The payment has been Deleted Successfully!'))
        return redirect('payments')


def add_receipt(request, username):
    if request.method == 'POST':
        form = DepitForm(request.POST)
        user = User.objects.get(username=username)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.description = request.POST['description']
            receipt.value = request.POST['value']
            receipt.user = user
            receipt.save()
            messages.success(
                request, ('The Receipt has been Added Successfully!'))
            return user_profile(request, username)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error ' + error_message))
            return user_profile(request, username)


def receipt_update(request, id):
    receipt = get_object_or_404(Depit, id=id)
    if request.method == 'POST':
        form = DepitForm(request.POST, instance=receipt)
        if form.is_valid():
            form.save()
            messages.success(
                request, ('The Receipt has been Updated Successfully!'))
            return receipt_profile(request, id)


def receipt_delete(request, id):
    receipt = get_object_or_404(Depit, id=id)
    if request.method == 'POST':
        receipt.delete()
        messages.success(
            request, ('The Receipt has been Deleted Successfully!'))
        return redirect('receipts')


def receipt_profile(request, id):
    receipt = Depit.objects.get(id=id)
    form = DepitForm(instance=receipt)

    return render(request, 'accounting/receipts/receipt_profile.html', {
        'receipt': receipt,
        'form': form,
    })


def receipts(request):
    receipts = Depit.objects.all()
    return render(request, 'accounting/receipts/receipts.html', {'receipts': receipts})


def user_receipts(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'accounting/receipts/user_receipts.html', context)
