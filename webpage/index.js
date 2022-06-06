let submitButton;
let nicknameInput;
let hiddenFrame;

function start() {
    submitButton = document.getElementById("submit-button");
    submitButton.addEventListener("click", registerUser, false);

    nicknameInput = document.getElementById("nickname");
    hiddenFrame = document.getElementById("hidden-frame");
}

function registerUser() {
    console.log("register");
    document.getElementById("form-nickname").value = nicknameInput.value;
    document.getElementById("reg-form").submit();
    window.location = "/chat"
}

window.addEventListener("load", start);