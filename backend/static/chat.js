let messageBox;
let messageInput;
let messageButton;
let userId;

function sendMessage() {
  let xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/message");
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.onload = () => {
    reloadChatRoom();
  };
  xmlhttp.send("user_id=" + getUserId() + "&message=" + messageInput.value);
  messageInput.value = "";
}

function getUserId() {
  return localStorage.getItem("user-id");
}

function reloadChatRoom() {
  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", "/message");

  xmlHttp.onload = () => {
    let messagesText = xmlHttp.responseText;
    let messages = JSON.parse(messagesText);

    let html = "";
    for (let i = 0; i < messages.length; i++) {
      html = "<label>" + messages[i]["msg"] + "</label><br>" + html;
    }
    messageBox.innerHTML = html;
  }
  xmlHttp.send(null);
}

function start() {
  userId = localStorage.getItem("user-id");
  // if user not registered, redirect to main page
  if (userId === null) {
    window.location = "/";
  }

  messageBox = document.getElementById("message-box");
  messageInput = document.getElementById("message-input");
  messageButton = document.getElementById("send-button");
  messageButton.addEventListener("click", sendMessage, false);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key == "Enter") {
      messageButton.click();
    }
  });
  reloadChatRoom();
  setInterval(reloadChatRoom, 300);
}

window.addEventListener("load", start);
