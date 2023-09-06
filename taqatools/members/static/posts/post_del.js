
function post_slug(slug) {
    const form = document.getElementById('post_del_form')
    form.setAttribute('action', `/post/${slug}/delete/`)
    const modal_open = document.getElementById('modal_button')
    modal_open.click()
}

