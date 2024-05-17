window.onload = function () {
    function togglePasswordVisibility() {
        var passwordInput = document.getElementById('password');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
        } else {
            passwordInput.type = 'password';
        }
    }
    
    function validateForm() {
        var nameField = document.getElementById('name');
        var emailField = document.getElementById('email');
        var passwordField = document.getElementById('password');
        var nameError = document.getElementById('nameError');
        var emailError = document.getElementById('emailError');
        var passwordError = document.getElementById('passwordError');
        var valid = true;

        nameError.innerHTML = '';
        emailError.innerHTML = '';
        passwordError.innerHTML = '';

        if (nameField.value.trim() === '') {
            nameError.innerHTML = 'Name is required';
            valid = false;
        }
        if (emailField.value.trim() === '') {
            emailError.innerHTML = 'Email is required';
            valid = false;
        } else if (!isValidEmail(emailField.value.trim())) {
            emailError.innerHTML = 'Invalid email address';
            valid = false;
        }
        if (passwordField.value.trim() === '') {
            passwordError.innerHTML = 'Password is required';
            valid = false;
        }
        if (valid) {
            // Prepare form data
            const formData = new FormData();
            formData.append('username', nameField.value.trim());
            formData.append('email', emailField.value.trim());
            formData.append('password', passwordField.value.trim());

            // Send AJAX request to the Flask server
            fetch('/register', {
                method: 'POST',
                body: formData
            })
                .then(response => response.text())
                .then(data => {
                    console.log(data); // Handle the response from the server
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }

    function isValidEmail(email) {
        // You can add your email validation logic here
        // For simplicity, let's assume any email is valid

        return true;
    }
};