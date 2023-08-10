from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json
from .models import Invoice
from .forms import InvoiceForm

# Create your views here.
def invoice_add(request):
    return render(request, 'accounts/invoices/invoices.html', {
        'name' : 'osama',
        'value': 37
    } )



def add_h1(request):
    data = request.POST
    name = data.get('name')
    value = data.get('value')
    form = InvoiceForm(request.POST)
    data_form = form.save(commit= False)
    data_form.name = name
    data_form.value = value
    data_form.save()
    print(name)
    count  = Invoice.objects.last()
    xxx = {
        'name': count.name,
        'value':count.value,
        'id' : count.id
    }
    xx = json.dumps(xxx)
    print(xx)
    success = f'the form has been submitted for {name} successfully, total ({count})'
    return HttpResponse(xx)

# test to repo synch