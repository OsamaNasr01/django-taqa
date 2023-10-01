
const pipe_submit = document.getElementById('pipe_submit')
pipe_submit.addEventListener('click', function (e) {
    e.preventDefault()
    const pipe_selection = document.getElementById('pipe_selection')
    const data_form = new FormData(pipe_selection)
    console.log(data_form.get('price'))
    if (pipe_submit.innerText === 'Remove from offer') {
        url = '/pump-offer/remove-pipe-from-offer/'
    } else {
        url = '/pump-offer/add-pipe-to-offer/'
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
        pipe_submit.className = "btn btn-danger form-control"
        pipe_submit.innerText = 'Remove from offer'

      } else {
        pipe_submit.className = "btn btn-primary form-control"
        pipe_submit.innerText = 'Add to offer'

      }
    })
    .catch((error) => {
        console.log(error)
    })


})
