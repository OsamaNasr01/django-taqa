
window.addEventListener('load', add_c_option())

function add_c_option() {
  const select = document.getElementById('id_category')
  const add_category_option = document.createElement('option')
  add_category_option.id = 'add_cat_op'
  add_category_option.addEventListener('click', function () {
    const cat_modal = document.getElementById('category_modal')
    cat_modal.click()
    console.log('clicked')
  })
  add_category_option.innerText = 'Add new Category'
  select.appendChild(add_category_option)
}

function remove_c_option() {
  const add_cat_option = document.getElementById('add_cat_op')
  add_cat_option.remove()

}

const category_submit = document.getElementById('category_submit')
category_submit.addEventListener('click', function (e) {
  e.preventDefault()
  var input_name = document.getElementById('input_name').value
  var input_description = document.getElementById('input_description').value
  const csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value
  const url = '/company/category/add/'

  const data = JSON.stringify({
      'name': input_name,
      'description': input_description,
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
        input_name= ""
        input_description= ""
        document.getElementById('modal_close').click()
         return response.json()
      } else {
      console.log(response)
      }
  })
  .then(data => {
    remove_c_option()
    const category = data['category']
    const select = document.getElementById('id_category')
    const new_category = document.createElement('option')
    new_category.value = category['id']
    new_category.innerText = category['name']
    new_category.selected = true
    select.appendChild(new_category)
    add_c_option()
    console.log(data)
  })
  .catch((error) => {
      console.log(error)
  })
})
