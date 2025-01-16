document.addEventListener("DOMContentLoaded", function() {
    // Check if there are errors on the username field
    const usernameErrors = document.querySelectorAll(".field-username .errorlist");
    const passwordErrors = document.querySelectorAll(".field-password1 .errorlist");

    // Show guidelines only if there are errors in the respective fields
    if (usernameErrors.length > 0) {
        document.getElementById("username-guidelines").style.display = "block";
    }

    if (passwordErrors.length > 0) {
        document.getElementById("password-guidelines").style.display = "block";
    }
});
