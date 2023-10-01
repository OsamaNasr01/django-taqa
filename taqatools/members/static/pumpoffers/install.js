
const install_submit = document.getElementById('install_submit')
install_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const install_selection = document.getElementById('install_selection')
    const data_form = new FormData(install_selection)
    console.log(data_form.get('price'))
    if (install_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-install-from-offer/'
    } else {
        url = '/pump-offer/add-install-to-offer/'
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
        install_submit.className = "btn btn-danger form-control"
        install_submit.innerText = 'Remove from offer'

      } else {
        install_submit.className = "btn btn-primary form-control"
        install_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
