let submitButton;

function start() {
    submitButton = document.getElementById("submit-button");
    submitButton.addEventListener("click", registerUser, false);
}

function registerUser() {
    console.log("register");
}

window.addEventListener("load", start);