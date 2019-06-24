window.onload = function()
{
    const logs = document.getElementById("logs_view");

    document.getElementById("btn").addEventListener('click', test);

    function test()
    {
        var rb1 = document.getElementById("rb1");
        var rb2 = document.getElementById("rb2");
        var rb3 = document.getElementById("rb3");
        var rb4 = document.getElementById("rb4");
        var model_fn = "";
        var model_sa = "";

        if (rb1.checked == true) {
            model_fn = "SVM - Fake News";
        }
        else if (rb2.checked == true) {
            
            model_fn = "Random Forest - Fake News";
        }
        
        if (rb3.checked == true) {
            model_sa = "SVM - Sentiment Analisys";
        }
        else if (rb4.checked == true) {
            model_sa = "Naive Bayes - Sentiment Analisys";
        }

        const data = JSON.stringify({
            "model_sa" : model_sa,
            "model_fn" : model_fn,
        })

        const api_url = "http://localhost:80/make_testnews";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }
}