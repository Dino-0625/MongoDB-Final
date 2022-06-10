let messageBox;
let messageInput;
let messageButton;
let userId;
let updateInterval;
let shiftPressed;
// to check if reload chatroom or not
let cachedHTML;

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
  messageButton.disabled = true;
  messageInput.value = "";
  autoHeight(messageInput);
}

function deleteMessage(msgId) {
  let request = new Request("/message", {
    method: "DELETE",
    headers: new Headers({
      "Content-Type": "application/json"
    }),
    body: JSON.stringify({ "user_id": getUserId(), "msg_id": msgId }),
  });

  fetch(request).then(() => reloadChatRoom());
}

function editMessage(msgId, new_msg) {
  let request = new Request("/message", {
    method: "PATCH",
    headers: new Headers({
      "Content-Type": "application/json"
    }),
    body: JSON.stringify({ "user_id": getUserId(), "msg_id": msgId, "new_msg": new_msg }),
  });

  fetch(request).then(() => reloadChatRoom());
}

function editMessageLabel(msgId) {
  let div = document.getElementById("msg-" + msgId);
  let textArea = document.createElement("textarea");
  // already in editing
  if (div.childElementCount != 0) {
    return;
  }

  textArea.classList = "form-control text-wrap";
  textArea.innerHTML = div.innerHTML;
  div.innerHTML = "";
  div.appendChild(textArea);

  autoHeight(textArea);
  textArea.addEventListener("keypress", (e) => {
    if (e.key == "Enter" && !e.shiftKey) {
      e.preventDefault();
      editMessage(parseInt(msgId), textArea.value);
      div.innerHTML = textArea.value;
    }
  });
  textArea.addEventListener("input", () => {
    autoHeight(textArea);
  })
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
      let msg = messages[i]["msg"];

      // deal with line break and spaces
      msg = msg.replace(/(?:\r\n|\r|\n)/g, "<br>").
        replace(/\s/g, "&nbsp;").replace("\t", "&emsp;");

      let my_id = localStorage.getItem("user-id");
      let dialog = "<div class='row'>";
      if (messages[i]["user_id"] == my_id) {
        // my message
        dialog += "<div class='user local'>";
        dialog += "<div class='text text-break' id='msg-" + messages[i]["_id"] + "'>";
        dialog += msg;
        dialog += "</div>";
        dialog += "<span class='msg-time'>" + msgTime + "</span>";
        dialog += "<span class='msg-time'><button class='btn btn-outline-dark' onclick='editMessageLabel(" +
          messages[i]["_id"] + ")'><img src='svg/pencil.svg' /></button>" +
          "<button class='btn btn-outline-danger' onclick='deleteMessage(" +
          String(messages[i]["_id"]) + ")'><img src='svg/trash.svg' /></button></span>";
        dialog += "</div>";
      } else {
        // not my message
        dialog += "<div class='user remote'>";
        dialog += "<div class='name'>";
        dialog += "<span style='font-size: large'>" + messages[i]["user_name"] +
          "</span><br><span style='font-size: x-small;'>#" +
          messages[i]["user_id"] + "</span>";
        dialog += "</div>";
        dialog += "<div class='text text-break'>";
        dialog += msg;
        dialog += "</div>";
        dialog += "<span class='msg-time'>" + msgTime + "</span>";
        dialog += "</div>";
      }
      dialog += "</div>";
      html = dialog + html;
    }

    // only update when not the same
    if (cachedHTML != html) {
      messageBox.innerHTML = html;
      messageBox.scrollTo(0, messageBox.scrollHeight);
      cachedHTML = html;
    }
  };
  xmlHttp.send(null);
}

function showInfoPage(userId) {
  document.getElementById("info-page").style.display = "block";
  document.getElementById("id-show").innerHTML = "ID:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;" + userId;
  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", "/user?" + "user_id=" + userId);
  xmlHttp.onload = () => {
    let res = JSON.parse(xmlHttp.responseText);
    document.getElementById("nickname-show").innerHTML = "暱稱:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;" + res["nickname"];
    document.getElementById("msg-count").innerHTML = "發送訊息總數:&emsp;&emsp;&emsp;&emsp;" + res["msg_count"];
    document.getElementById("char-count").innerHTML = "發送訊息總字元數:&emsp;&emsp;" + res["char_count"];
    document.getElementById("avg-len").innerHTML = "平均每則訊息字元數:&emsp;" + res["avg_len"];
  };
  xmlHttp.send(null);
}

function start() {
  messageBox = document.getElementById("message-box");
  messageInput = document.getElementById("message-input");
  messageButton = document.getElementById("send-button");
  messageButton.addEventListener("click", sendMessage, false);
  messageInput.addEventListener(
    "keydown",
    (e) => {
      // press shift key + enter means new line
      if (e.key == "Enter" && !e.shiftKey) {
        // preventDefault: prevent generating new line
        e.preventDefault();
        messageButton.click();
      }
    },
    false
  );
  messageInput.addEventListener(
    "input",
    () => {
      messageButton.disabled = messageInput.value.replace(/(?:\r\n|\r|\n)/g, "").length == 0;
      if (messageInput.value.length >= 5000) {
        messageInput.value = messageInput.value.substring(0, 5000);
      }
      autoHeight(messageInput);
    },
    false
  );
  reloadChatRoom();
  // updateInterval = setInterval(reloadChatRoom, 300);
}

function autoHeight(elem) {  /* javascript */
  elem.style.height = "1px";
  elem.style.height = (elem.scrollHeight + 2) + "px";
}

// if user not registered, redirect to main page
userId = localStorage.getItem("user-id");
if (userId === null) {
  window.location = "/";
}

window.addEventListener("load", start);
