import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    if mars == None:
        result = redirect("http://localhost:5000/scrape")
    else:
        result = render_template("index.html", mars=mars)
    return result


@app.route("/scrape")
def crawl():
    mars = mongo.db.mars
    mars_data = scrape_mars.crawler()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/")


if __name__ == "__main__":
    app.run(debug=True)
