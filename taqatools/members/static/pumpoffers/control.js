

function control_submit(id) {
  const submit_btn = document.getElementById(`control_submit_${id}`)
  const control_selection = document.getElementById(`control_selection_${id}`)
  const data_form = new FormData(control_selection)
  console.log(data_form.get('price'))
  if (submit_btn.innerText === 'Remove from offer') {
      url = '/pump-offer/remove-control-from-offer/'
  } else {
      url = '/pump-offer/add-control-to-offer/'
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
      submit_btn.innerText = 'Remove from offer'

    } else {
      submit_btn.className = "btn btn-primary form-control"
      submit_btn.innerText = 'Add to offer'

    }
  })
  .catch((error) => {
      console.log(error)

})
}
