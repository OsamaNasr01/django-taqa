from django.shortcuts import render, HttpResponse, redirect
from .forms import PumpOfferRequestForm
from .models import PumpOfferRequest, PumpOffer
from members.forms import AddAddressForm
from members.models import Gov, City, Company
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
        return redirect('home')
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
    

def create_offer(request):
    offer = PumpOffer.objects.create(
        company = Company.objects.get(owner = request.user), 
        request = PumpOfferRequest.objects.get(id = request.POST['request_id']),
        value = 0,
        )
    offer.save()
    return render(request, 'pumpoffers/response/pump.html', {'offer':offer})

 
def pump_selection(request):
    
    return render(request, 'pumpoffers/response/pump.html', {})

def motor_selection(request):
    return render(request, 'pumpoffers/response/motor.html', {})

def pipes_selection(request):
    return render(request, 'pumpoffers/response/pipes.html', {})

def adaptors_selection(request):
    return render(request, 'pumpoffers/response/adaptors.html', {})

def cable_selection(request):
    return render(request, 'pumpoffers/response/cable.html', {})

def control_panel_selection(request):
    return render(request, 'pumpoffers/response/control_panel.html', {})

def install_evaluatation(request):
    return render(request, 'pumpoffers/response/installation.html', {})