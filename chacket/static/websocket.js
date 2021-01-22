const msgerChat = document.querySelector(".msger-chat");
const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
let client_id = Date.now()
let ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

function sendMessage(event) {
    let input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}

ws.onmessage = function appendMessage(event) {
    const msgHTML = `
                    <div class="msg right-msg">
                      <div class="msg-img" style="background-image: url(${BOT_IMG})"></div>
                      <div class="msg-bubble">
                        <div class="msg-info">
                          <div class="msg-info-name">Chelik</div>
                          <div class="msg-info-time">${formatDate(new Date())}</div>
                        </div>
                        <div class="msg-text">${event.data}</div>
                      </div>
                    </div>
                  `;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}
