window.onload = function()
{
    const logs = document.getElementById("logs_view");
    var interval = null;

    document.getElementById("btn").addEventListener('click', retrain);

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

    function check_logs()
    {
        const data = JSON.stringify({
            "logs" : "raw",
        })
        const api_url = "http://localhost:80/make_train_logs";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.responseText == "FINISHED") {
                clearInterval(interval);
            }
            else if (this.readyState == 4 && this.status == 200) {
                logs.innerHTML = this.responseText.replace(/\n/g, "<br>");
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }

    function retrain()
    {
        var rb1 = document.getElementById("rb1");
        var rb2 = document.getElementById("rb2");
        var rb3 = document.getElementById("rb3");
        var rb4 = document.getElementById("rb4");
        var model = "";

        if (rb1.checked == true) {
            model = "SVM - Fake News";
        }
        else if (rb2.checked == true) {
            model = "SVM - Sentiment Analisys";
        }
        else if (rb3.checked == true) {
            model = "Random Forest - Fake News";
            
        }
        else if (rb4.checked == true) {
            model = "Naive Bayes - Sentiment Analisys";
        }

        const data = JSON.stringify({
            "model" : model,
            "username" : username_to_show,
        })

        if (username_to_show == undefined) {
            alert("You are not logged in. You need administrator privileges to use this feature!");
        }
        const api_url = "http://localhost:80/make_train";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if (this.responseText == "OK") {
                    alert("Model will start the training! Check out logs below!");
                    interval = setInterval(function(){
                        check_logs()
                    }, 1000);
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