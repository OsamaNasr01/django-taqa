
const valid = document.getElementById('id_valid')
const taxes = document.getElementById('id_include_taxes')
const trans = document.getElementById('id_include_trans')
const installment = document.getElementById('id_installment')
const offer_id = document.getElementById('offer_id')

valid.addEventListener('change', function(){
    console.log(valid.value)
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/validity/'
    const data = JSON.stringify({
        'offer_id': offer_id.value,
        'validity': valid.value
    })
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        'body': data,
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
        console.log('ok')
    })
    .catch((error) => {
        console.log(error)
    })
})


taxes.addEventListener('change', function(){
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/taxes/'
    const data = JSON.stringify({
        'offer_id': offer_id.value,
        'taxes': taxes.checked
    })
    console.log(data)
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        'body': data,
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
        console.log('ok')
    })
    .catch((error) => {
        console.log(error)
    })
})



trans.addEventListener('change', function(){
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/transport/'
    const data = JSON.stringify({
        'offer_id': offer_id.value,
        'trans': trans.checked
    })
    console.log(data)
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        'body': data,
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
        console.log('ok')
    })
    .catch((error) => {
        console.log(error)
    })
})


installment.addEventListener('change', function(){
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/installment/'
    const data = JSON.stringify({
        'offer_id': offer_id.value,
        'installment': installment.checked
    })
    console.log(data)
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        'body': data,
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
        console.log('ok')
    })
    .catch((error) => {
        console.log(error)
    })
})
