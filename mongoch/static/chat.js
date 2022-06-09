let messageBox;
let messageInput;
let messageButton;
let userId;
let updateInterval;

function sendMessage() {
  let xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", "/message");
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.onload = () => {
    reloadChatRoom();
  };
  xmlhttp.send(
    "user_id=" +
      getUserId() +
      "&message=" +
      encodeURIComponent(messageInput.value)
  );
  messageInput.value = "";
  messageButton.disabled = true;
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
      let msgTime = new Date(messages[i]["date"]).toLocaleTimeString();
      let time = msgTime.split(":");
      time = time.slice(0, time.length - 1);
      msgTime = time.join(":");

      // html = "<label class='user-name'>" +
      //   messages[i]["user_name"] + "(" + messages[i]["user_id"] + ")" +
      //   ":</label><label class='rounded-pill bg-fill'>" +
      //   "&nbsp;&nbsp;" + messages[i]["msg"] + "&nbsp;&nbsp;" +
      //   "</label><label class='time-label'>" +
      //   msgTime +
      //   "</label><br>" +
      //   html;
      let my_id = localStorage.getItem("user-id");
      let dialog = "";
      dialog += "<div class='dialogue'>";
      if (messages[i]["user_id"] == my_id) {
        //my message
        dialog += "<div class='user local'>";
        dialog += "<div class='avatar'>";
        dialog += "<div class='name'>";
        dialog += messages[i]["user_name"];
        dialog += "</div></div>";
        dialog += "<div class='text'>";
        dialog += messages[i]["msg"];
        dialog += "</div></div>";
      } else {
        //not my message
        dialog += "<div class='user remote'>";
        dialog += "<div class='avatar'>";
        dialog += "<div class='name'>";
        dialog += messages[i]["user_name"];
        dialog += "</div></div>";
        dialog += "<div class='text'>";
        dialog += messages[i]["msg"];
        dialog += "</div></div>";
      }
      dialog += "</div>";
      html = dialog + html;
    }
    messageBox.innerHTML = html;
    messageBox.scrollTo(0, messageBox.scrollHeight);
  };
  xmlHttp.send(null);
}

function start() {
  messageBox = document.getElementById("message-box");
  messageInput = document.getElementById("message-input");
  messageButton = document.getElementById("send-button");
  messageButton.addEventListener("click", sendMessage, false);
  messageInput.addEventListener(
    "keypress",
    (e) => {
      if (e.key == "Enter") {
        messageButton.click();
      }
    },
    false
  );
  messageInput.addEventListener(
    "input",
    () => {
      messageButton.disabled = messageInput.value.length == 0;
    },
    false
  );
  reloadChatRoom();
  // updateInterval = setInterval(reloadChatRoom, 300);
}

// if user not registered, redirect to main page
userId = localStorage.getItem("user-id");
if (userId === null) {
  window.location = "/";
}

window.addEventListener("load", start);
