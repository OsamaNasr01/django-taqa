from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import requests
import json
import webbrowser

# Create your views here.
@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        gate = request.POST['gate']
        if gate == '1':
            return payment_proccess(request, gate)
        else:
            return render(request, 'payments/wallet_input.html', {})
    else:
        return render(request, 'payments/checkout.html', {})

@login_required(login_url='login')
def payment_proccess(request, gate):
    token = get_token()
    order_id = make_order(token  )
    payment_token = request_payment_key(token, order_id, gate)
    if gate == '2':
        wallet_no = request.POST['wallet_no']
        url = wallet_pay_request(payment_token, wallet_no)
        # webbrowser.open(url)
    else:
        url = card_pay_request(payment_token)
        # webbrowser.open(url)
    return redirect(url)
    

    
api_key = 'ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SndjbTltYVd4bFgzQnJJam8zTVRZd016a3NJbU5zWVhOeklqb2lUV1Z5WTJoaGJuUWlMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuUHVXVVh1NUlUdDQ2NjdFVmV1YUdzVkZwb0JmQm56N0NFRmtiLVMzNFNmazRnQkhQX3Fxb24yU0R4RkRzeklISDM5c3FJSWE4MUVqcm50LWNvd3k4WUE='

def get_token():
    data = {
        'api_key': api_key,
    }

    url = 'https://accept.paymob.com/api/auth/tokens'
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        response.raise_for_status()

        response_data = response.json()
        token = response_data.get('token')
        if token:
            return token
        else:
            print("Token not found in response.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




def make_order(token):
    data = {
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": "5000",
        "currency": "EGP",
        "items": [],
    }

    url = 'https://accept.paymob.com/api/ecommerce/orders'

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        response.raise_for_status()

        response_data = response.json()
        order_id = response_data.get('id')

        if order_id:
            return order_id
        else:
            print("Order ID not found in response.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




def request_payment_key(token, order_id, gate):
    if gate == '2':
        int_id = '3544185'
    elif gate == '1':
        int_id = '3544186'

    data = {
        "auth_token": token,
        "amount_cents": "1000",
        "expiration": 3600,
        "order_id": order_id,
        "billing_data": {
            "apartment": "NA",
            "email": "osama.nasr.01@gmail.com",
            "floor": "NA",
            "first_name": "Osama",
            "street": "NA",
            "building": "NA",
            "phone_number": "01027476938",
            "shipping_method": "NA",
            "postal_code": "NA",
            "city": "NA",
            "country": "Eg",
            "last_name": "Nasr",
            "state": "NA"
        },
        "currency": "EGP",
        "integration_id": int_id,
    }

    url = 'https://accept.paymob.com/api/acceptance/payment_keys'

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        response.raise_for_status()

        response_data = response.json()
        payment_token = response_data.get('token')

        if payment_token:
            return payment_token
        else:
            print("Payment token not found in response.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")



def wallet_pay_request(payment_token, wallet_no):
    data = {
        "source": {
            "identifier": wallet_no,
            "subtype": "WALLET"
        },
        "payment_token": payment_token,
    }

    url = 'https://accept.paymob.com/api/acceptance/payments/pay'

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        response.raise_for_status()

        response_data = response.json()
        iframe_redirection_url = response_data.get('iframe_redirection_url')

        if iframe_redirection_url:
            return iframe_redirection_url
        else:
            print("IFrame redirection URL not found in response.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




def card_pay_request(payment_token):
    url = f'https://accept.paymob.com/api/acceptance/iframes/740313?payment_token={payment_token}'
    return url



def payment_status(request):
    return render(request, 'payments/status.html', {})