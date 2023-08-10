from django.shortcuts import render

# Create your views here.

def accounting(request):
    return render(request, 'accounting/invoices/accounting_panel.html', {})


def add_s_invoice(request):
    return render(request, 'accounting/invoices/add_s_invoice.html', {} )