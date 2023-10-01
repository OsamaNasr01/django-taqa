
function change_price(id) {
    const offer_total_value = document.getElementById('offer_value')
    const price_value = document.getElementById(`price_${id}`)
    const q_value = document.getElementById(`q_${id}`)
    const item_total_value = document.getElementById(`item_total_${id}`)
    console.log(price_value.value)
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/change-item-price/'
    const data = JSON.stringify({
        'item_id': id,
        'new_price': price_value.value
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
        item_total_value.innerText = data['item_value'].toLocaleString ({minimumFractionDigits: 2})
        offer_total_value.innerText = data['offer_value'].toLocaleString ({minimumFractionDigits: 2})
    })
    .catch((error) => {
        console.log(error)
    })
}


function change_q(id) {
    const offer_total_value = document.getElementById('offer_value')
    const price_value = document.getElementById(`price_${id}`)
    const q_value = document.getElementById(`q_${id}`)
    const item_total_value = document.getElementById(`item_total_${id}`)
    console.log(price_value.value)
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/pump-offer/change-item-q/'
    const data = JSON.stringify({
        'item_id': id,
        'new_q': q_value.value
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
        item_total_value.innerText = data['item_value'].toLocaleString ({minimumFractionDigits: 2})
        offer_total_value.innerText = data['offer_value'].toLocaleString ({minimumFractionDigits: 2})
    })
    .catch((error) => {
        console.log(error)
    })
}
