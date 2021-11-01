# use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

# use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo

# to use the scraping code, we will convert from Jupyter notebook to Python
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define Flask route for HTML page, telling Flask what to display when we're looking at the home page, index.html 
# tells Flask what to display when we're looking at the home page, index.html
@app.route("/")
def index():
   # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script
   mars = mongo.db.mars.find_one()
   # tells Flask to return an HTML template using an index.html file, tells Python to use the "mars" collection in MongoDB
   return render_template("index.html", mars=mars)

# Define Flask route for scraping
# defines the route that Flask will be using
@app.route("/scrape")
# Define the function
def scrape():
    # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # create a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # update the database
    mars.update({}, mars_data, upsert=True)
    # add a redirect after successfully scraping the data which will navigate our page back to / where we can see the updated content
    return redirect('/', code=302)

# Tell Flask to run
if __name__ == "__main__":
   app.run()
    
