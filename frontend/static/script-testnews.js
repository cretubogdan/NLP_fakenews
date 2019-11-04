window.onload = function()
{
    const logs = document.getElementById("logs_view");

    document.getElementById("btn").addEventListener('click', test);
    var rb1 = document.getElementById("rb1");
    var rb2 = document.getElementById("rb2");
    var rb3 = document.getElementById("rb3");
    var rb4 = document.getElementById("rb4");
    const title = document.getElementById("title");
    const author = document.getElementById("author")
    const text = document.getElementById("text");

    var COOKIES = {};
    var cookieStr = document.cookie;
    cookieStr.split(/; /).forEach(function(keyValuePair) {
        var cookieName = keyValuePair.replace(/=.*$/, "");
        var cookieValue = keyValuePair.replace(/^[^=]*\=/, "");
        COOKIES[cookieName] = cookieValue;
    });
    if (!(COOKIES["title"] == undefined)) {
        document.getElementById("title").value = COOKIES["title"];
    }
    if (!(COOKIES["author"] == undefined)) {
        document.getElementById("author").value = COOKIES["author"];
    }
    if (!(COOKIES["text"] == undefined)) {
        document.getElementById("text").value = COOKIES["text"];
    }

    var username_to_show = COOKIES["username"];

    if (username_to_show == undefined) {
        document.getElementById("log-in-show-id").innerHTML = "Not logged in";
    }
    else {
        document.getElementById("log-in-show-id").innerHTML = "Logged in as: " + username_to_show;
    }


    function test()
    {
        var model_fn = "Random Forest - Fake News";
        var model_sa = "Naive Bayes - Sentiment Analisys";

        if (rb1.checked == true) {
            model_fn = "SVM - Fake News";
        }
        else if (rb3.checked == true) {
            model_fn = "Random Forest - Fake News";
        }
        
        if (rb2.checked == true) {
            model_sa = "SVM - Sentiment Analisys";
        }
        else if (rb4.checked == true) {
            model_sa = "Naive Bayes - Sentiment Analisys";
        }

        const data = JSON.stringify({
            "model_sa" : model_sa,
            "model_fn" : model_fn,
            "title" : title.value,
            "author" : author.value,
            "text" : text.value,
        })

        if (username_to_show == undefined) {
            alert("You are not logged in. You have to be logged in to use this feature!");
        }
        else {
            const api_url = "http://localhost:80/make_testnews";
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    logs.innerHTML = this.responseText.replace(/\n/g, "<br>");
                }
            };
            xhttp.open("POST", api_url, true);
            xhttp.setRequestHeader("Content-Type", "application/json");
            xhttp.send(data);
        }
    }
}
