from django.shortcuts import render
from .forms import PurchaseInvoiceForm

# Create your views here.

def accounting(request):
    return render(request, 'accounting/invoices/accounting_panel.html', {})


def add_s_invoice(request):
    invoice_form = PurchaseInvoiceForm()
    return render(request, 'accounting/invoices/add_s_invoice.html', {
        'invoice_form': invoice_form,
    } )