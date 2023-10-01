
const motor_submit = document.getElementById('motor_submit')
motor_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const motor_selection = document.getElementById('motor_selection')
    const data_form = new FormData(motor_selection)
    console.log(data_form.get('price'))
    if (motor_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-motor-from-offer/'
    } else {
        url = '/pump-offer/add-motor-to-offer/'
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
        motor_submit.className = "btn btn-danger form-control"
        motor_submit.innerText = 'Remove from offer'

      } else {
        motor_submit.className = "btn btn-primary form-control"
        motor_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
