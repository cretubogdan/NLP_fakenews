window.onload = function()
{
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const email = document.getElementById("email");

    document.getElementById("btn").addEventListener('click', login);

    function login()
    {
        const data = JSON.stringify({
            "username" : username.value,
            "password" : password.value,
            "email" : email.value,
        });

        const api_url = "http://localhost:80/make_signup";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                if (this.responseText == "OK") {
                    username.value = "";
                    password.value = "";
                    email.value = "";
                    alert("Sign up successfully");
                }
                else {
                    alert(this.responseText);
                }
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }
}
