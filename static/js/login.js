window.onload = function() {
    document.getElementById('eye-button').addEventListener('click', function() {
        var passwordField = document.getElementById('password-field');
        var eyeButton = document.getElementById('eye-button');

        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            eyeButton.style.backgroundImage = 'url("./assets/images/login/open-eye.png")';
        } else {
            passwordField.type = 'password';
            eyeButton.style.backgroundImage = 'url("./assets/images/login/eye.png")';
        }
    });
};