window.onload = function()
{
    const logs = document.getElementById("logs_view");

    document.getElementById("btn").addEventListener('click', retrain);

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
        })

        const api_url = "http://localhost:80/make_train";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if (this.responseText == "OK") {
                    alert("Model will start the training! Check out logs below!");
                    console.log(this.responseText);
                }
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }
}