// Control Sign when One form is already opened
document.addEventListener("DOMContentLoaded", function() {
    const signInButton = document.getElementById("signInButton");
    const modals = ["signUpModal", "forgotPasswordModal"];

    modals.forEach((modalId) => {
        const modalElement = document.getElementById(modalId);

        if (modalElement) {
            // Disable Sign In button when any specified modal is shown
            modalElement.addEventListener("show.bs.modal", function () {
                signInButton.classList.add("disabled");
                signInButton.setAttribute("aria-disabled", "true");
            });

            // Enable Sign In button when the modal is hidden
            modalElement.addEventListener("hidden.bs.modal", function () {
                signInButton.classList.remove("disabled");
                signInButton.removeAttribute("aria-disabled");
            });
        }
    });
});


// control the flash Message
document.addEventListener("DOMContentLoaded", function() {
    // Find all flash messages
    const flashMessages = document.querySelectorAll(".flash-message");

    // Set a timer to remove each flash message after 10 seconds
    flashMessages.forEach((flashMessage) => {
        setTimeout(() => {
            // Use Bootstrap's built-in fade out effect by toggling the 'show' class
            flashMessage.classList.remove("show");
        }, 10000); // 10 seconds = 10000 milliseconds
    });
});