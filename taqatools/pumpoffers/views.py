from django.shortcuts import render, HttpResponse
from .forms import PumpOfferRequestForm
from members.forms import AddAddressForm
from members.models import Gov, City
import json
# Create your views here.



def pump_offer_request(request):
    if request.method == 'POST':
        pass
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
        