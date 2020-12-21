function toggle_follow(id) {
    fetch(`../follow/${id}`)
    .then(request => {
        window.location.reload()
    })
}