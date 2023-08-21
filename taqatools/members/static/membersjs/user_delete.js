
function username(username) {
    const form = document.getElementById('user_del_form')
    form.setAttribute('action', `/members/${username}/delete/`)
    const modal_open = document.getElementById('modal_button')
    modal_open.click()
}

