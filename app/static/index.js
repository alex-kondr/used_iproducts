const username = document.getElementById("username")
const password = document.getElementById("password")
const formData = new URLSearchParams()
const button = document.getElementById("button")
button.addEventListener("click", () => {
    console.log("username.value=", username.value)
    console.log("password", password.value)
    formData.append("username", username.value)
    formData.append("password", password.value)
    console.log(formData)
    fetch("/users/token/", {
        method: "POST",
        body: formData,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status} - ${response.statusText}`)
            }
            return response.json();
        })
        .then(data => {
            localStorage.setItem("access_token", data.access_token)
            console.log("Success:", data)
            window.location.href = "/web/users/";
        })
})