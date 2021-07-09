from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.Mars_db
Mars_collection = db.Mars_collection


#Trying alternate method to connect to Mongo
# app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_db"
# mongo = PyMongo(app)

@app.route("/")
def index():
    #Storing Mars data in a list 
    # Mars = Mars_collection.find()
    Mars = mongo.db.Mars_collection.find_one()
    # Rendering it into index
    return render_template("index.html", Mars=Mars)


@app.route("/scrape")
def scraper():
    print("Inside the scrape route")
    #added first line to test new mongo
    Mars = mongo.db.Mars_collection
    Mars_data = scrape_mars.scrape()
    print(Mars_data)
    # Mars_collection.drop()
    Mars.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)
    

if __name__ == "__main__":
    app.run(debug=True)