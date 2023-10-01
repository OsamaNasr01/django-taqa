
const cable_submit = document.getElementById('cable_submit')
cable_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const cable_selection = document.getElementById('cable_selection')
    const data_form = new FormData(cable_selection)
    console.log(data_form.get('price'))
    if (cable_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-cable-from-offer/'
    } else {
        url = '/pump-offer/add-cable-to-offer/'
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
        cable_submit.className = "btn btn-danger form-control"
        cable_submit.innerText = 'Remove from offer'

      } else {
        cable_submit.className = "btn btn-primary form-control"
        cable_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
