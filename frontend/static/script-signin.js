window.onload = function()
{
    const username = document.getElementById("username");
    const password = document.getElementById("password");

    document.getElementById("btn").addEventListener('click', login);

    var COOKIES = {};
    var cookieStr = document.cookie;
    cookieStr.split(/; /).forEach(function(keyValuePair) {
        var cookieName = keyValuePair.replace(/=.*$/, "");
        var cookieValue = keyValuePair.replace(/^[^=]*\=/, "");
        COOKIES[cookieName] = cookieValue;
    });

    var username_to_show = COOKIES["username"];

    if (username_to_show == undefined) {
        document.getElementById("log-in-show-id").innerHTML = "Not logged in";
    }
    else {
        document.getElementById("log-in-show-id").innerHTML = "Logged in as: " + username_to_show;
    }

    function login()
    {
        const data = JSON.stringify({
            "username" : username.value,
            "password" : password.value,
        });

        if (username_to_show == undefined) {
            const api_url = "http://localhost:80/make_signin";
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    console.log(this.responseText);
                    if (this.responseText == "OK") {
                        document.cookie = "username=" + username.value;
                        alert("Sign in successfully");
                        document.getElementById("log-in-show-id").innerHTML = "Logged in as: " + username.value;
                        username.value = "";
                        password.value = "";
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
        else {
            alert("You are aleardy logged in as: " + username_to_show);
        }
    }
}
