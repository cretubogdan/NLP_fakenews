window.onload = function()
{
    const table = document.getElementById("news_table");
    table.innerHTML = (make_header() + "</table>");

    function make_header()
    {
        var html_to_add = "";

        html_to_add += "<table>";
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
            "count_news" : "2",
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
            }
        };
        xhttp.open("POST", api_url, true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(data);
    }
}