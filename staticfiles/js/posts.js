function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.querySelectorAll('.like-form').forEach(form => {
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const postId = this.dataset.postId;
        const csrftoken = getCookie('csrftoken');
        const heartIcon = this.querySelector('.heart-icon');
        const likeCountSpan = this.querySelector('.like-count');

        const response = await fetch(`/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const data = await response.json();
            likeCountSpan.textContent = data.likes;

            // Toggle heart color
            if (data.liked) {
                heartIcon.classList.add('text-red-500', 'fill-current');
                heartIcon.classList.remove('text-gray-500');
            } else {
                heartIcon.classList.remove('text-red-500', 'fill-current');
                heartIcon.classList.add('text-gray-500');
            }
        }
    });
});



