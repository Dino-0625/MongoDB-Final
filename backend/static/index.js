let submitButton;
let nicknameInput;

function start() {
    submitButton = document.getElementById("submit-button");
    submitButton.addEventListener("click", registerUser, false);

    nicknameInput = document.getElementById("nickname");
}

// do http post
function registerUser() {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "/user");
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.onload = function () {
        localStorage.setItem("user-id", xmlhttp.responseText);
        // redirect to chat room
        window.location = "/chat";
    }
    xmlhttp.send("nickname=" + nicknameInput.value);
}

window.addEventListener("load", start);
