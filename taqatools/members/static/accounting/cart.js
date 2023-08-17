
const json_data = document.getElementById('json_data').value
const data  = JSON.parse(json_data)
const items = data['items']
console.log(data['items'])
const cart_items_table = document.getElementById('cart_items')
const table_head = document.getElementById('table_head')
const cart_total = document.getElementById('cart_total')
cart_total.innerText = data['total'].toLocaleString ({minimumFractionDigits: 2})
for (var item in items) {
    const item_data = items[item]
    const table_row = document.createElement('tr')
    table_row.setAttribute('id', items[item].id)
    const td_f = document.createElement('td')
    td_f.innerText = item
    table_row.appendChild(td_f)
    for (var key in item_data) {
        const td = document.createElement('td')
        if ( key === 'name') {
            const link  = document.createElement('a')
            link.setAttribute('href', `/product/${item_data['slug']}`)
            link.innerText = item_data[key]
            td.appendChild(link)
            table_row.appendChild(td)
        } else if ( key === 'id') {
            const delete_item = document.createElement('button')
            delete_item.setAttribute('onclick', `del_item(${item_data[key]})`)
            delete_item.setAttribute('class', 'btn')
            delete_item.classList.add('btn-danger')
            delete_item.classList.add('btn-sm')
            delete_item.innerText = 'delete'
            delete_item.id = 'delete_item'
            delete_item.setAttribute('name', `${item_data[key]}`)
            td.setAttribute('style', 'width:10%')
            td.appendChild(delete_item)
            table_row.appendChild(td)
        } else if ( key === 'slug') {

        } else if ( key === 'price') {
            td.setAttribute('id', `price_${item_data['id']}`)
            td.innerText = item_data[key].toLocaleString ({minimumFractionDigits: 2})
            table_row.appendChild(td)
        } else if (key === 'total') {
            td.setAttribute('id', `total_${item_data['id'].toFixed}`)
            td.innerText = item_data[key].toLocaleString ({minimumFractionDigits: 2})
            table_row.appendChild(td)
        } else if ( key === 'no') {    
            const no_input = document.createElement('input')
            no_input.setAttribute('type', 'number')
            td.setAttribute('style', 'width:15%')
            no_input.setAttribute('class', 'form-control')
            no_input.setAttribute('onchange', `change_item_q(${item_data['id']})`)
            no_input.value = item_data[key]
            no_input.id = `input_${item_data['id']}`
            td.appendChild(no_input)
            table_row.appendChild(td)

        } else {
            td.innerText = item_data[key]
            table_row.appendChild(td)
        }
    }
    cart_items_table.appendChild(table_row)
}

function del_item(id) {
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    console.log(csrftoken)

    const url = '/cart/delete_cart_item/'
    const data = JSON.stringify({
        'item_id': id,
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
            const element = document.getElementById(id)
            cart_items_table.removeChild(element)
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
        console.log(Object.keys(data).length)
        const navbar_cart = document.getElementById('cart-navbar')
        navbar_cart.innerText = `Cart (${Object.keys(data['items']).length})`
        cart_total.innerText = data['total']
    })
    .catch((error) => {
        console.log(error)
    })
}

function change_item_q(id) {
    const new_q = document.getElementById(`input_${id}`).value
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
    const url = '/cart/update_cart_item/'

    const data = JSON.stringify({
        'item_id': id,
        'new_q': new_q
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
        const item_total = document.getElementById(`total_${id}`)
        const item_price = document.getElementById(`price_${id}`).innerText
        item_total.innerText = `${new_q*item_price}`
        cart_total.innerText = data['total']
    })
    .catch((error) => {
        console.log(error)
    })
}



const search_box = document.getElementById('search')
search_box.addEventListener('input', function() {
    const query = search_box.value
    const user_list = document.getElementById('user-list')
    user_list.innerHTML = ""
    if (query !== '' ) {
        const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
        const url = '/cart/search-users/'
        const data = JSON.stringify({
            'query': query,
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
            for (var user in data) {
                const op = document.createElement('option')
                op.innerText = data[user]
                user_list.appendChild(op)
            }
        })
        .catch((error) => {
        })

    }
})


const offer_submit = document.getElementById('offer_submit')
offer_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const full_name = search_box.value
    const user_name = full_name.split(' ')
    const username = user_name.pop()
    console.log(username)
    const description = document.getElementById('description').value
    const cart_total_value = cart_total.innerText
    console.log(cart_total_value)
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value

    if (offer_form.name === 'offer_form') {
        var url = '/cart/add-offer/'
    } else if (offer_form.name === 'sale_form') {
        var url = '/cart/add-sale/'
    } else if (offer_form.name === 'purchase_form') {
        var url = '/cart/add-purchase/'
    }
    const data = JSON.stringify({
        'user_name': username,
        'description' : description,
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
            console.log(response)
            const close_modal = document.getElementById('close_modal').click()
            const cart_div = document.getElementById('cart_div')
            cart_div.innerHTML= ""
            const h3 = document.createElement('h3')
            h3.innerText = 'Offer is submitted and Cart is impty'
            cart_div.appendChild(h3)
            return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
    })
    .catch((error) => {
        console.log(error)
    })



})


function add(type) {
    const offer_form = document.getElementById('offer_form')
    offer_form.name = `${type}_form`
}
