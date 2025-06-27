const tbody = document.getElementById("tbody")
const tr = document.createElement("tr")
const accessToken = localStorage.getItem("access_token")
const addElementWithText = (parent, childElementName, text) => {
    const child = document.createElement(childElementName)
    child.textContent = text
    parent.appendChild(child)
}
fetch("/users/me/", {
    headers: {
        "Authorization": `Bearer ${accessToken}`
    }
})
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log("data=", data)
        addElementWithText(tr, "td", data.id)
        addElementWithText(tr, "td", data.username)
        addElementWithText(tr, "td", data.active)
        tbody.appendChild(tr)
    });


const buttonOpen = document.getElementById("connectButton")
const buttonClose = document.getElementById("disconnectButton")
const messageText = document.getElementById("sendMessage")
const buttonSend = document.getElementById("sendButton")
const answerText = document.getElementById("messages")

buttonOpen.addEventListener("click", function () {
    // Замініть "ws://example.com" на URL вашого WebSocket сервера
    const serverUrl = document.getElementById("serverUrl")
    const friendName = document.getElementById("friendName")
    const socket = new WebSocket(`${serverUrl.value}/${friendName.value}/${accessToken}/`);

    // Обробник події відкриття з'єднання
    socket.onopen = function (event) {
        console.log("WebSocket з'єднання встановлено");
        buttonOpen.style.visibility = "hidden"
        buttonClose.style.visibility = "visible"
        messageText.removeAttribute("disabled")
        buttonSend.removeAttribute("disabled")
        socket.send("Привіт, сервер!\n"); // Відправка повідомлення на сервер
    };

    buttonSend.addEventListener("click", function () {
        socket.send(messageText.value)
    })
    // Обробник події отримання повідомлень
    socket.onmessage = function (event) {
        console.log("Отримано повідомлення:", event.data);
        const p = document.createElement("p")
        p.textContent = event.data
        answerText.appendChild(p)
    };

    // Обробник події помилки
    socket.onerror = function (event) {
        console.error("WebSocket помилка:", event);
    };


    // Щоб закрити з'єднання:
    buttonClose.addEventListener("click", function () {
        // Обробник події закриття з'єднання
        socket.onclose = function (event) {
            buttonOpen.style.visibility = "visible"
            buttonClose.style.visibility = "hidden"
            console.log("WebSocket з'єднання закрито", event);
        };
        socket.close();
    })
    // socket.close();
})
