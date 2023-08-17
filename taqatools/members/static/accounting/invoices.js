
const name = document.getElementById('name')
const value = document.getElementById('value')
const url = '/invoice/add_h1/'
const csrfToken = '{{csrf_token}}';

document.getElementById('post').onclick = () => {
  const  requestObj = new XMLHttpRequest()
  requestObj.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText)
      const resTxt = this.responseText
      const backData = JSON.parse(resTxt);
      console.log(backData)
      const div = document.getElementById('output')
      p = document.createElement('p')
      y = document.createElement('p')
      z = document.createElement('p')
      p.innerHTML = backData.name
      y.innerHTML = backData.value
      z.innerHTML = backData.id
      div.appendChild(p)
      div.appendChild(y)
      div.appendChild(z)
      name.value = ""
      value.value = ""
    }
  }
  requestObj.open("POST", '/invoice/add_h1/')
  requestObj.setRequestHeader("X-CSRFToken", csrfToken)
  const formdata = new FormData()
  formdata.append('name', name.value)
  formdata.append('value', value.value)
  requestObj.send(formdata)
  console.log(this.responseText)
}
