function toggle_follow(id) {
    fetch(`../follow/${id}`)
    .then(request => {
        window.location.reload()
    })
}

function edit_post_form(clicked_id) {
    let post = document.querySelector(`#post_${clicked_id}`)
    let header = post.querySelector('#header').textContent
    let text = post.querySelector('#text').textContent
    post.innerHTML = `<form id="edit-form-${clicked_id}">
    <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">Header</label>
      <input id="header" type="text" class="form-control" id="exampleFormControlInput1"">
    </div>
    <div class="mb-3">
      <label for="exampleFormControlTextarea1" class="form-label">Post</label>
      <textarea id="text" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
    </div>
    <div class="col-auto">
      <button type="submit" class="btn btn-primary mb-3">Save</button>
    </div>
  </form>`
    post.querySelector('#header').value = header
    post.querySelector('#text').value = text
    document.querySelector(`#edit-form-${clicked_id}`).onsubmit = () => edit_post(clicked_id)
}

function edit_post(id) {
    let form = document.querySelector(`#edit-form-${id}`)
    let post = {
        header: form.querySelector('#header').value,
        text: form.querySelector('#text').value,
    }
    fetch(`/edit/${id}`, {
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(post)
    })
        .then(() => window.location.reload())
}