
from flask import Flask, jsonify, render_template, url_for, redirect
from flask_pymongo import PyMongo
import mission_to_mars as mtm

import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(engine, reflect=True)

# Save reference to the table
#Station = Base.classes.station
#Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")

#################################################
# Flask Routes
#################################################


@app.route("/")
@app.route("/home")
def welcome():
    # pull information from the mongo db
    pictures = mongo.db.mars_pic.find()
    news = mongo.db.mars_news.find_one()
    images = mongo.db.mars_img.find_one()
    
    return render_template('index.html', pictures=pictures, news=news, mars_img=images)


@app.route("/about")
def about():

    images = mongo.db.mars_img.find_one()
    return render_template('about.html', title='About', mars_img=images)

@app.route("/data")
def data():

    images = mongo.db.mars_img.find_one()
    # data = mongo.db.mars_data.find_one()
    with open('Resources/mars_facts.html', 'r') as file:
        data = file.read()

    return render_template('data.html', title='Mars Data', mars_img=images, data=data)


@app.route("/scrape_feature_image")
def scrape_feature_image():

    # Run the scrape function
    img_data = mtm.scrape_feature_image()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_img.update({}, img_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/scrape_latest_news")
def scrape_latest_news():

    # Run the scrape function
    news = mtm.scrape_latest_news()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_news.update({}, news, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/scrape_mars_data")
def scrape_mars_data():
    # Run the scrape function
    mars_data = mtm.scrape_mars_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Return template and data
    return redirect("/data")

@app.route("/scrape_mars_hemi")
def scrape_mars_hemi():

    # Run the scrape function
    hemisphere = mtm.scrape_mars_hemi()
    #hemisphere = [{'title': 'Cerberus Hemisphere Enhanced', 'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
    #  {'title': 'Schiaparelli Hemisphere Enhanced', 'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, 
    # {'title': 'Syrtis Major Hemisphere Enhanced', 'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}, 
    # {'title': 'Valles Marineris Hemisphere Enhanced', 'url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]

    for hemi_dict in hemisphere:

        # Update the Mongo database using update and upsert=True
        mongo.db.mars_pic.update(hemi_dict, hemi_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
