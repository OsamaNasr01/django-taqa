
function new_brand() {
    document.getElementById('product_modal_close').click()
    setTimeout(document.getElementById('brand_modal').click(),10)
  }
  const brand_submit = document.getElementById('brand_submit')
  brand_submit.addEventListener('click', function(e) {
    e.preventDefault()
    url = '/product/brand/add/'
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value

    let image_file = document.getElementById('brand_image').files[0]

    let form_data = new FormData()
    form_data.append('name', document.getElementById('brand_name').value)
    form_data.append('country', document.getElementById('brand_country').value)
    form_data.append('description', document.getElementById('brand_description').value)
    form_data.append('category', document.getElementById('brand_category').value)
    form_data.append('image', image_file)
    console.log(form_data)
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrftoken,
        },
        'body': form_data,
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