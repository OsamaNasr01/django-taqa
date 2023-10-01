
const control_submit = document.getElementById('control_submit')
control_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const control_selection = document.getElementById('control_selection')
    const data_form = new FormData(control_selection)
    console.log(data_form.get('price'))
    if (control_submit.innerText === 'Remove from offer') {
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
        control_submit.className = "btn btn-danger form-control"
        control_submit.innerText = 'Remove from offer'

      } else {
        control_submit.className = "btn btn-primary form-control"
        control_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
