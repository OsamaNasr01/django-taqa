
const btn = document.getElementById('add_to_cart')
const product_id = document.getElementById('product_id').value
const csrftoken =  document.querySelector('[name="csrfmiddlewaretoken"]').value;
const url = '/accounting/add-product-to-cart/'
btn.onclick = () => {
  const no = document.getElementById('no').value
  const data = JSON.stringify({
    'product_id': product_id,
    'no': no,
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
    console.log(data['cart_items'])
    const navbar_cart = document.getElementById('cart-navbar')
    const message = document.getElementById('messege')
    message.innerText = data['message']
    navbar_cart.innerText = 'Cart (' + data['cart_items'] + ')'
  })
  .catch((error) => {
    console.log(error)
  })
  console.log(csrftoken)
  if (btn.className === "btn btn-danger") {
    btn.className = "btn btn-primary"
    btn.innerHTML = "Add To Cart"
  } else {
    if (btn.className === "btn btn-primary") {
      btn.className = "btn btn-danger"
      btn.innerHTML = "Remove from Cart"
    }
  }
}
