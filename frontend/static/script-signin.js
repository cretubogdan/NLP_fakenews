window.onload = function()
{
    const username = document.getElementById("username");
    const password = document.getElementById("password");

    document.getElementById("btn").addEventListener('click', login);

    function login()
    {
        const data = JSON.stringify({
            "username" : username.value,
            "password" : password.value,
        });

        const api_url = "http://localhost:80/make_signin";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                if (this.responseText == "OK") {
                    username.value = "";
                    password.value = "";
                    alert("Sign in successfully");
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
