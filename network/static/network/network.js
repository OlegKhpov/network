document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#posts-form').onsubmit = () => create_post()
    let likes_array = document.querySelectorAll('#like-data')
    likes_array.forEach(element => {
        let element_id = element.querySelector('a').id
        fetch(`like/check/${element_id}`)
            .then(json => json.json())
            .then(response => {
                if (response['result'] === true) {
                    element.querySelector('a').setAttribute('style', 'color: red')
                }
            })
    });
});


function create_post() {
    let post = {
        header: document.querySelector('#header').value,
        text: document.querySelector('#text').value,
    }
    fetch(`/posts/create`, {
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(post)
    })
        .then(() => window.location.reload())

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

function toggle_like(like_link) {
    let post_id = like_link.id
    let counter = document.querySelector(`#like-count-${post_id}`)
    fetch(`toggle_like/${post_id}`)
        .then(json => json.json())
        .then(response => {
            if (response['message'] === true) {
                like_link.setAttribute('style', 'color: red')
                counter.textContent = parseInt(counter.textContent, 10) + 1
            } else {
                like_link.setAttribute('style', 'color: lightblue')
                counter.textContent = parseInt(counter.textContent, 10) - 1
            }
        })
}

