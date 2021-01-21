from bs4 import BeautifulSoup
import requests
import pandas as pd


def crawler():
    article_info = mars_news()
    mars_info = {}
    mars_info["article_title"] = article_info[0]
    mars_info["article_description"] = article_info[1]
    mars_info["featured_image"] = mars_featured_image()
    mars_info["weather"] = mars_weather()
    mars_info["facts"] = mars_facts()
    mars_info["hemispheres"] = mars_hemispheres()
    return mars_info


def mars_news():
    news = []
    URL = (
        "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=1&order="
        + "publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    )
    r = requests.get(URL)

    if r.status_code == 200:
        news = [
            {"title": rec["title"], "description": rec["description"]}
            for rec in r.json()["items"]
        ]
    title = [rec["title"] for rec in news]
    description = [rec["description"] for rec in news]
    article = [title[0], description[0]]
    return article


def mars_featured_image():
    r = requests.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    soup = BeautifulSoup(r.text, "html.parser")
    featured_image = soup.find("article")["style"].split("'")
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image[1]
    return featured_image_url


def mars_weather():
    r = requests.get("https://twitter.com/marswxreport?lang=en")
    soup = BeautifulSoup(r.text, "html.parser")
    weather = soup.find("p", class_="tweet-text").text.split("pic.twitter")
    return weather[0]


def mars_facts():
    facts = pd.read_html("https://space-facts.com/mars/")
    facts_df = pd.DataFrame(facts[0])
    facts_df.columns = ["Description", "Value"]
    facts_html = facts_df.to_html(header=False, index=False)
    return facts_html


def mars_hemispheres():
    r = requests.get(
        "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    mars_hemisphere_data = []
    soup = BeautifulSoup(r.text, "html.parser")
    hemispheres = soup.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        info_url = "https://astrogeology.usgs.gov" + hemisphere.find("a")["href"]
        r = requests.get(info_url)
        soup = BeautifulSoup(r.text, "html.parser")
        image_url = (
            "https://astrogeology.usgs.gov"
            + soup.find("img", class_="wide-image")["src"]
        )
        mars_hemisphere_data.append({"title": title, "img_url": image_url})
    return mars_hemisphere_data

print(crawler())
