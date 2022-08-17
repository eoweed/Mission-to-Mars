# ----------------------------------
# import dependencies
# ----------------------------------
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask app
app = Flask(__name__)

# connect python and mongo with PyMongo
# Use flask_pymongo to set up connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# ----------------------------------
# set up app routes
# ----------------------------------
# home page route
@app.route("/")
def index():
    # find the 'mars' collectionName in mongo
    mars = mongo.db.mars.find_one()
    # use render template on the index.html file with the mars collection
    return render_template('index.html', mars=mars)

# scrape route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run()

