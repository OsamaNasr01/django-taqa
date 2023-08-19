
function new_brand() {
    document.getElementById('product_modal_close').click()
    setTimeout(document.getElementById('brand_modal').click(),10)
  }
  const brand_submit = document.getElementById('brand_submit')
  brand_submit.addEventListener('click', function(e) {
    e.preventDefault()
    url = '/product/brand/add/'
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value

    const data = JSON.stringify({
      'name': document.getElementById('brand_name').value,
      'country': document.getElementById('brand_country').value,
      'description' : document.getElementById('brand_description').value,
      'category': document.getElementById('brand_category').value,
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
          back2_product()
          console.log(response)
          return response.json()
        } else {
        console.log(response)
        }
    })
    .then(data => {
      console.log(data)
      add_bran_op(data)
    })
    .catch((error) => {
        console.log(error)
    })
  })


  function back2_product () {
    document.getElementById('brand_name').value =""
    document.getElementById('brand_country').value = ""
    document.getElementById('brand_description').value = ""
    document.getElementById('brand_modal_close').click()
    setTimeout(document.getElementById('product_modal').click(),10)

  }

  function add_bran_op (data) {
    const select = document.getElementById('id_brand')
    const new_brand = document.createElement('option')
    new_brand.value = data['brand_id']
    new_brand.innerText = data['brand_name']
    new_brand.selected = true
    select.appendChild(new_brand)

  }