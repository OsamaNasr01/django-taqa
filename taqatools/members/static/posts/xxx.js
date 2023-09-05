
const post_form = document.getElementById('form_id')
post_form.addEventListener('submit', function (e) {
    e.preventDefault
    url = '/posts/add-post'
    fetch(url, {
        'method' : 'POST',
        'body': new FormData(post_form),
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
      post_form.remove()
      const messege_id = document.getElementById('messege_id')
      messege_id.innerText = data['messege']
      post_submit.remove()
      console.log(data['messege'])
    })
    .catch((error) => {
        console.log(error)
    })
})
