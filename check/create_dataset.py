import requests
import csv
import time
import newspaper
from bs4 import BeautifulSoup

link_label = []
dataset = []
sites = ["nytimes.com", "slate.com", "foxnews.com", "cnn.com"]
count = 1

with open("link_label") as f:
    lines = f.readlines()
    for line in lines:
        stuff = line.split()
        link_label.append((stuff[0], stuff[1]))

for (link, label) in link_label:
    article = newspaper.Article(link)
    data = requests.get(link).text
    article.set_html(data)
    article.parse()
    article.nlp()
    news = article.text

    lines = (line.strip() for line in news.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    news = '\n'.join(chunk for chunk in chunks if chunk)

    print(news + "\n")
    dataset.append((count, news, label))
    count += 1

    time.sleep(5)


with open('news_sa.csv', mode='w') as news_sa:
    news_sa_writer = csv.writer(news_sa, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for (index, data, label) in dataset:
        news_sa_writer.writerow([index, data, label])