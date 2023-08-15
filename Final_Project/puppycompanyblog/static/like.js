document.addEventListener('DOMContentLoaded', function() {
    let buttons = document.querySelectorAll('.react-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let postId = button.getAttribute('data-post-id');
            let userId = button.getAttribute('data-user-id');
            let reaction = button.getAttribute('data-reaction');

            fetch(`/post/${postId}/reaction`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: userId,
                    reaction_type: reaction
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                // Here you can update the UI, for instance increment/decrement like/dislike count.
            });
        });
    });
});
