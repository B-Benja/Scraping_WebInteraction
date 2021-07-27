from bs4 import BeautifulSoup
import requests


SITE = "https://news.ycombinator.com/news"

response = requests.get(SITE).text
soup = BeautifulSoup(response, "html.parser")


articles = soup.find_all(name="a", class_="storylink")
#soup.select_one(".storylink").getText()

article_texts = []
article_links = []
for article in articles:
    text = article.getText()
    article_texts.append(text)
    link = article.get("href")
    article_links.append(link)

article_upvote = []
upvote = soup.find_all(name="td", class_="subtext")
for article in upvote:
    votes = article.find(name="span", class_="score")
    if votes is None:
        article_upvote.append(0)
    else:
        article_upvote.append(int(votes.string.split()[0]))

# get the most upvoted text and article link
print(article_texts[article_upvote.index(max(article_upvote))])
print(article_links[article_upvote.index(max(article_upvote))])