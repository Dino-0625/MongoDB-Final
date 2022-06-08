let submitButton;
let nicknameInput;

function start() {
  // let userId = localStorage.getItem("user-id");
  // // if user id created, redirect to chatroom
  // if (userId) {
  //   window.location = "/chat";
  // }

  submitButton = document.getElementById("submit-button");
  submitButton.addEventListener("click", registerUser, false);
  nicknameInput = document.getElementById("nickname");
  nicknameInput.addEventListener("keypress", (e) => {
    if (e.key == "Enter") {
      submitButton.click();
    }
  });
}

// do http post
function registerUser() {
  let xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/user");
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.onload = () => {
    localStorage.setItem("user-id", xmlhttp.responseText);
    // redirect to chat room
    window.location = "/chat";
  };
  xmlhttp.send("nickname=" + nicknameInput.value);
}

window.addEventListener("load", start);
