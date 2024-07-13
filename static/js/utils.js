function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function reloadPost(postId, html) {
    const post = document.getElementById(`post${postId}`);
    post.outerHTML = html;
    initFlowbite();
}

function likePost(postId) {
    fetch(`/api/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => response.text())
        .then(response => reloadPost(postId, response))
        .catch((error) => console.log(error));
}

function deletePost(postId) {
    fetch(`/api/posts/${postId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(() => document.getElementById(`post${postId}`).remove())
        .catch(() => document.getElementById(`post${postId}`).remove());
}

function addComment(postId) {
    const post = document.getElementById(`post${postId}`);
    const contentTextarea = post.querySelector(`[name="content${postId}"]`);
    const content = contentTextarea.value.trim();

    if (!content) {
        contentTextarea.focus();
        return;
    }

    fetch(`/api/posts/${postId}/comments/`, {
        method: 'POST',
        body: JSON.stringify({content}),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.text())
        .then(response => reloadPost(postId, response))
        .catch((error) => console.log(error));
}

function deleteComment(postId, commentId) {
    fetch(`/api/comments/${commentId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
        .then(response => response.text())
        .then(response => reloadPost(postId, response))
        .catch((error) => console.log(error));
}
