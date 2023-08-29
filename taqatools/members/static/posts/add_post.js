
const post_submit = document.getElementById('post_submit')
post_submit.addEventListener('click', function (e) {
    e.preventDefault
    url = '/posts/add-post'
    const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value

    const data = JSON.stringify({
      'title': document.getElementById('title').value,
      'content': document.getElementById('content').value,
      'category' : document.getElementById('category').value,
    })
    fetch(url, {
        'method' : 'POST',
        'headers' : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        'body': data,
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
      const post_form = document.getElementById('form_id')
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
