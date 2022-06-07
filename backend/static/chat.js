let messageBox;

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function reloadChatRoom() {
    let messages = httpGet("/message");
    console.log(messages);
}

function start() {
    messageBox = document.getElementById("message-box");
    reloadChatRoom();
}

window.addEventListener("load", start);
