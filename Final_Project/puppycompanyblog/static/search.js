$(document).ready(function() {
    $("#userSearchForm").submit(function(e) {
        e.preventDefault();
        let username = $("#usernameInput").val();
        
        // Redirect to the user's profile page
        window.location.href = `http://127.0.0.1:5000/${username}`;
    });
});
