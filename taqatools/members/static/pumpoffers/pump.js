
const pump_submit = document.getElementById('pump_submit')
pump_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const pump_selection = document.getElementById('pump_selection')
    const data_form = new FormData(pump_selection)
    console.log(data_form.get('price'))
    if (pump_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-pump-from-offer/'
    } else {
        url = '/pump-offer/add-pump-to-offer/'
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
        pump_submit.className = "btn btn-danger form-control"
        pump_submit.innerText = 'Remove from offer'

      } else {
        pump_submit.className = "btn btn-primary form-control"
        pump_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
