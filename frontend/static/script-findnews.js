window.onload = function()
{
    const table = document.getElementById("news_table");
    table.innerHTML = (make_header() + "</table>");

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
    
    function make_header()
    {
        var html_to_add = "";

        html_to_add += "<table id=\"mytable\">";
        html_to_add += "<tr>";
        html_to_add += "<th>Title</th>";
        html_to_add += "<th>Author</th>";
        html_to_add += "<th>Text</th>";
        html_to_add += "</tr>";

        return html_to_add;
    }

    document.getElementById("btn").addEventListener('click', find);

    function find()
    {
        const data = JSON.stringify({
            "count_news" : "1",
        })

        const api_url = "http://localhost:80/make_findnews";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                var array_news = JSON.parse(this.responseText).results;
                var news_length = array_news.length;
                var html_to_add = "";

                html_to_add = make_header();
                for (var i = 0;i < news_length;i++) {
                    html_to_add += "<tr>";
                    html_to_add  += "<td>" + array_news[i].title + "</td>";
                    html_to_add  += "<td>" + array_news[i].author + "</td>";
                    html_to_add  += "<td>" + array_news[i].body + "</td>";
                    html_to_add  += "</tr>";
                }
                html_to_add  += "</table>";

                table.innerHTML = html_to_add;

                var my_table = document.getElementById("mytable");
                var rows = my_table.getElementsByTagName("tr");
                for (i = 0;i < rows.length; i++) {
                    var currentRow = my_table.rows[i];
                    var createClickHandler = function(row) {
                        return function () {
                            document.cookie = "title=" + row.getElementsByTagName("td")[0].innerHTML;
                            document.cookie = "author=" + row.getElementsByTagName("td")[1].innerHTML;
                            document.cookie = "text=" + row.getElementsByTagName("td")[2].innerHTML;
                            location.replace("http://localhost/testnews")
                        };
                    };
                    currentRow.onclick = createClickHandler(currentRow);
                }
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }
}