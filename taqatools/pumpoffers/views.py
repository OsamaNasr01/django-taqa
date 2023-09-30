from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import PumpOfferRequestForm
from .models import PumpOfferRequest, PumpOffer, PumpOfferItem
from members.forms import AddAddressForm
from members.models import Gov, City, Company
from products.models import Product, Category
import json
from django.contrib.auth.decorators import login_required
# Create your views here.



@login_required(login_url='login')
def pump_offer_request(request):
    if request.method == 'POST':
        address_form = AddAddressForm(request.POST)
        new_address = address_form.save(commit=False)
        new_address.city = City.objects.get(id=request.POST['city'])
        new_address.details = request.POST['details']
        new_address.save()
        offer_request_form = PumpOfferRequestForm(request.POST)
        new_request = offer_request_form.save(commit=False)
        new_request.user = request.user
        new_request.address = new_address
        new_request.save()
        return redirect('pumpoffer_request_list')
    else:
        address_form = AddAddressForm()
        form = PumpOfferRequestForm()
        return render(request, 'pumpoffers/pump_offer_request.html', {
            'form' : form,
            'address_form' : address_form,
            'govs': Gov.objects.all()
        })
        
        
def gov_select(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        gov_id = data['gov_id']
        cities = City.objects.filter(gov=gov_id)
        return_data = {}
        for city in cities:
            return_data[city.id] = city.name
        
        json_data = json.dumps(return_data)
        print(json_data)
        return HttpResponse(json_data, content_type="application/json") 
        
def pumpoffer_request_list(request):
    requests = PumpOfferRequest.objects.all()
    return render(request, 'pumpoffers/pumpoffer_request_list.html', {'requests': requests})


def pumpoffer_request_profile(request, id):
    offer_request = PumpOfferRequest.objects.get(id=id)
    return render(request, 'pumpoffers/request_profile.html', {'offer_request': offer_request})
    

def pump_selection(request):
    offer = PumpOffer.objects.create(
        company = Company.objects.get(owner = request.user), 
        request = PumpOfferRequest.objects.get(id = request.POST['request_id']),
        )
    offer.save()
    pumps = Product.objects.filter(category = Category.objects.get(id = 15 ))
    return render(request, 'pumpoffers/response/pump.html', {
        'offer':offer,
        'pumps':pumps,
        })

def add_pump_to_offer(request):
    offer_pump = PumpOfferItem.objects.create(
        product = Product.objects.get(id = request.POST['pump_id']),
        offer = PumpOffer.objects.get(id = request.POST['offer_id']),
        q = request.POST['q'],
        price = request.POST['price'],
    )
    offer_pump.save()
    json_data = json.dumps({'data':'added'})
    return HttpResponse(json_data, content_type="application/json")


def remove_pump_from_offer(request):
    offer_pump = PumpOfferItem.objects.get(
        product_id =request.POST['pump_id'], 
        offer_id =  request.POST['offer_id'],
        )
    offer_pump.delete()
    json_data = json.dumps({'data':'removed'})
    return HttpResponse(json_data, content_type="application/json")
    



def motor_selection(request):
    offer = PumpOffer.objects.get(id=request.POST['offer_id'])
    motors = Product.objects.filter(category = Category.objects.get(id = 3 ))
    for motor in motors:
        print(motor.name)
    return render(request, 'pumpoffers/response/motor.html', {
        'offer':offer,
        'motors':motors,
        })

def add_motor_to_offer(request):
    offer_motor = PumpOfferItem.objects.create(
        product = Product.objects.get(id = request.POST['motor_id']),
        offer = PumpOffer.objects.get(id = request.POST['offer_id']),
        q = request.POST['q'],
        price = request.POST['price'],
    )
    offer_motor.save()
    json_data = json.dumps({'data':'added'})
    return HttpResponse(json_data, content_type="application/json")


def remove_motor_from_offer(request):
    offer_motor = PumpOfferItem.objects.get(
        product_id =request.POST['motor_id'], 
        offer_id =  request.POST['offer_id'],
        )
    offer_motor.delete()
    json_data = json.dumps({'data':'removed'})
    return HttpResponse(json_data, content_type="application/json")
    


def pipe_selection(request):
    offer = PumpOffer.objects.get(id=request.POST['offer_id'])
    pipes = Product.objects.filter(category = Category.objects.get(id = 16 ))
    return render(request, 'pumpoffers/response/pipes.html', {
        'offer':offer,
        'pipes':pipes,
        })

def add_pipe_to_offer(request):
    offer_pipe = PumpOfferItem.objects.create(
        product = Product.objects.get(id = request.POST['pipe_id']),
        offer = PumpOffer.objects.get(id = request.POST['offer_id']),
        q = request.POST['q'],
        price = request.POST['price'],
    )
    offer_pipe.save()
    json_data = json.dumps({'data':'added'})
    return HttpResponse(json_data, content_type="application/json")


def remove_pipe_from_offer(request):
    offer_pipe = PumpOfferItem.objects.get(
        product_id =request.POST['pipe_id'], 
        offer_id =  request.POST['offer_id'],
        )
    offer_pipe.delete()
    json_data = json.dumps({'data':'removed'})
    return HttpResponse(json_data, content_type="application/json")


def adaptor_selection(request):
    offer = PumpOffer.objects.get(id=request.POST['offer_id'])
    adaptors = Product.objects.filter(category = Category.objects.get(id = 17 ))
    return render(request, 'pumpoffers/response/adaptors.html', {
        'offer':offer,
        'adaptors':adaptors,
        })

def add_adaptor_to_offer(request):
    offer_adaptor = PumpOfferItem.objects.create(
        product = Product.objects.get(id = request.POST['adaptor_id']),
        offer = PumpOffer.objects.get(id = request.POST['offer_id']),
        q = request.POST['q'],
        price = request.POST['price'],
    )
    offer_adaptor.save()
    json_data = json.dumps({'data':'added'})
    return HttpResponse(json_data, content_type="application/json")


def remove_adaptor_from_offer(request):
    offer_adaptor = PumpOfferItem.objects.get(
        product_id =request.POST['adaptor_id'], 
        offer_id =  request.POST['offer_id'],
        )
    offer_adaptor.delete()
    json_data = json.dumps({'data':'removed'})
    return HttpResponse(json_data, content_type="application/json")

def cable_selection(request):
    return render(request, 'pumpoffers/response/cable.html', {})

def control_panel_selection(request):
    return render(request, 'pumpoffers/response/control_panel.html', {})

def install_evaluatation(request):
    return render(request, 'pumpoffers/response/installation.html', {})