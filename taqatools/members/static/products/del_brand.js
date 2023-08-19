
function brand_slug(slug) {
    url = `/product/brand/delete/${slug}/`
    const brand_del_form = document.getElementById('del_brand_form')
    brand_del_form.setAttribute("action", url)
  }
