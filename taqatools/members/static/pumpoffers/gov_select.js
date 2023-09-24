
const gov = document.getElementById('id_gov')
gov.addEventListener('change', function (value) {
  console.log(gov.value)
  
  url = '/pump-offer/gov-select/'
  const csrftoken =  document.querySelector('[name="csrfmiddlewaretoken"]').value;
  
  const data = JSON.stringify({
    'gov_id': gov.value,
  })
  console.log(data)
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
      return response.json()
    } else {
      console.log(response)
    }
  })
  .then(data => {
    console.log(data)
    const city = document.getElementById('id_city')
    city.innerHTML = ''
    for (var key in data) {
      const option = document.createElement('option')
      option.value = key
      option.innerText = data[key]
      city.appendChild(option)
    }
  })
  .catch((error) => {
    console.log(error)
  })
  })

