
from flask import Flask, jsonify, render_template, url_for, redirect
from flask_pymongo import PyMongo
import mission_to_mars as mtm

import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")

#################################################
# Flask Routes
#################################################

# main page
@app.route("/")
@app.route("/home")
def welcome():
    # pull information from the mongo db
 
    news = mongo.db.mars_news.find_one()
    images = mongo.db.mars_img.find_one()
    
    return render_template('index.html', news=news, mars_img=images)

# An about page to talk about the web site.
@app.route("/about")
def about():

    images = mongo.db.mars_img.find_one()
    return render_template('about.html', title='About', mars_img=images)

# Web page to show the statistics
@app.route("/data")
def data():

    images = mongo.db.mars_img.find_one()
    data = mongo.db.mars_data.find_one()

    return render_template('data.html', title='Mars Data', mars_img=images, data=data)

# HTML page to show the hemispheres
@app.route("/hemi")
def hemi():

    images = mongo.db.mars_img.find_one()
    pictures = mongo.db.mars_pic.find()

    return render_template('hemi.html', title='Mars Hemispheres', mars_img=images, pictures=pictures)

# The following routes are used to scrape information from the web pages.
@app.route("/scrape_feature_image")
def scrape_feature_image():

    # Run the scrape function to get the image
    img_data = mtm.scrape_feature_image()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_img.update({}, img_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/scrape_latest_news")
def scrape_latest_news():

    # Run the scrape function to get the latest news
    news = mtm.scrape_latest_news()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_news.update({}, news, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/scrape_mars_data")
def scrape_mars_data():
    # Run the scrape function to get the mars statistics
    mars_data = mtm.scrape_mars_data()
    
    data_dict = {'filename' : mars_data}

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, data_dict, upsert=True)

    # Return template and data
    return redirect("/data")

@app.route("/scrape_mars_hemi")
def scrape_mars_hemi():

    # Run the scrape function to get the pictures of the hemispheres
    hemisphere = mtm.scrape_mars_hemi()
    
    for hemi_dict in hemisphere:

        # Update the Mongo database using update and upsert=True
        mongo.db.mars_pic.update(hemi_dict, hemi_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/scrape_all")
def scrape_all():

    # Run the scrape function to get the image
    img_data = mtm.scrape_feature_image()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_img.update({}, img_data, upsert=True)

    # Run the scrape function to get the latest news
    news = mtm.scrape_latest_news()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_news.update({}, news, upsert=True)

    # Run the scrape function to get the mars statistics
    mars_data = mtm.scrape_mars_data()
    
    data_dict = {'filename' : mars_data}

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, data_dict, upsert=True)

    # Run the scrape function to get the pictures of the hemispheres
    hemisphere = mtm.scrape_mars_hemi()
    
    for hemi_dict in hemisphere:

        # Update the Mongo database using update and upsert=True
        mongo.db.mars_pic.update(hemi_dict, hemi_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
