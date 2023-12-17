
  
function product_submit(id) {
  const submit_btn = document.getElementById(`product_submit_${id}`)
  const product_selection = document.getElementById(`product_selection${id}`)
  const data_form = new FormData(product_selection)
  console.log(data_form.get('price'))
  if (submit_btn.innerText === 'حذف من العرض') {
      url = '/tender-offer/remove-product/'
  } else {
      url = '/tender-offer/add-product/'
  }
  fetch(url, {
      'method' : 'POST',
      'body': data_form,
  }) 
  .then(response => {
      if (response.ok) {
        console.log(response)
        return response.json()
      } else {
      console.log(response)
      }
  })
  .then(data => {
    console.log(data)
    if (data['data'] === 'added') {
      submit_btn.className = "btn btn-danger form-control"
      submit_btn.innerText = 'حذف من العرض'

    } else {
      submit_btn.className = "btn btn-primary form-control"
      submit_btn.innerText = 'اضف الي العرض'

    }
  })
  .catch((error) => {
      console.log(error)

})
}

