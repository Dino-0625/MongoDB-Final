let submitButton;
let nicknameInput;
let hiddenFrame;

function start() {
    submitButton = document.getElementById("submit-button");
    submitButton.addEventListener("click", registerUser, false);

    nicknameInput = document.getElementById("nickname");
    hiddenFrame = document.getElementById("hidden-frame");
}

// do http post
function registerUser() {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("post", "/user");
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("nickname=" + nicknameInput.value);
    console.log(xmlhttp.responseText);
}

window.addEventListener("load", start);
