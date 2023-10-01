
const adaptor_submit = document.getElementById('adaptor_submit')
adaptor_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const adaptor_selection = document.getElementById('adaptor_selection')
    const data_form = new FormData(adaptor_selection)
    console.log(data_form.get('price'))
    if (adaptor_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-adaptor-from-offer/'
    } else {
        url = '/pump-offer/add-adaptor-to-offer/'
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
        adaptor_submit.className = "btn btn-danger form-control"
        adaptor_submit.innerText = 'Remove from offer'

      } else {
        adaptor_submit.className = "btn btn-primary form-control"
        adaptor_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
